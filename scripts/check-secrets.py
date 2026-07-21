#!/usr/bin/env python3
"""Redacted secret scanning for public repository content, history, and artifacts."""

from __future__ import annotations

import argparse
import hashlib
import io
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
MAX_CONTENT_SIZE = 20 * 1024 * 1024

PATTERNS = {
    "private key": re.compile(
        r"-----BEGIN (?:RSA |DSA |EC |OPENSSH |ENCRYPTED )?PRIVATE KEY-----"
    ),
    "JWT-like token": re.compile(
        r"\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}\b"
    ),
    "Google API key": re.compile(r"\b(?P<google_api_key>AIza[0-9A-Za-z_-]{30,})\b"),
    "Google OAuth client secret": re.compile(r"\bGOCSPX-[0-9A-Za-z_-]{20,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "GitLab token": re.compile(r"\bglpat-[0-9A-Za-z_-]{20,}\b"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{20,}\b"),
    "Stripe live secret": re.compile(r"\bsk_live_[0-9A-Za-z]{20,}\b"),
    "SendGrid API key": re.compile(r"\bSG\.[0-9A-Za-z_-]{16,}\.[0-9A-Za-z_-]{16,}\b"),
    "npm token": re.compile(r"\bnpm_[0-9A-Za-z]{30,}\b"),
    "PyPI token": re.compile(r"\bpypi-[0-9A-Za-z_-]{30,}\b"),
    "Supabase service-role assignment": re.compile(
        r"(?i)(?:service[_-]?role|supabase[_-]?service[_-]?key)\s*[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9._-]{20,}"
    ),
    "hard-coded password assignment": re.compile(
        r"(?i)(?:password|passwd)"
        r"\s*[\"']?\s*[:=]\s*(?:\"(?P<password_double>[^\"\r\n]{8,})\"|"
        r"'(?P<password_single>[^'\r\n]{8,})'|(?P<password_bare>[A-Za-z0-9_+/=-]{20,}))"
    ),
    "hard-coded secret assignment": re.compile(
        r"(?i)(?:api[_-]?key|client[_-]?secret|secret|token)"
        r"\s*[\"']?\s*[:=]\s*(?:\"(?P<secret_double>[^\"\r\n]{8,})\"|"
        r"'(?P<secret_single>[^'\r\n]{8,})'|(?P<secret_bare>[A-Za-z0-9_+/=-]{20,}))"
    ),
    "credential in URL": re.compile(
        r"(?i)https?://[^/\s:@]+:[^/\s@]{8,}@[^\s/]+"
    ),
}

# SHA-256 fingerprints of exact values Rein inspected and confirmed are public
# placeholders. The values themselves are intentionally not duplicated here.
CLASSIFIED_VALUE_DIGESTS = {
    "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f": "user-confirmed placeholder",
    "51647453dbd335603e2cbeb79e292d238be203db07a439935784ff545ac0b718": "user-confirmed placeholder",
    "3fc894b249cfcccc508110a3136659e2ffa833db4fdece65760d1e8916241ad9": "publishable Google client configuration",
    "978daba98268972ba23f1b19fc2d3903bf9cf2a86692ae665f92dd4f747cc269": "publishable Google client configuration",
    "aa3cad2953148923d574cdb45f0f6cb00c4d2231e6c5e22e68d9587636055911": "publishable Google client configuration",
    "c3c11c79942db27958876de37c9ff132e57d9c4bb89083ea3a0709a19b71bcbd": "publishable Google client configuration",
}

findings: set[tuple[str, str]] = set()
classifications: set[tuple[str, str]] = set()
coverage_errors: set[str] = set()
FALLBACK_ASSIGNMENT_LABELS = {
    "hard-coded password assignment",
    "hard-coded secret assignment",
}


def safe_locator(locator: str) -> str:
    """Return a scope plus opaque identifier without emitting path content."""
    candidate = re.sub(r"[^a-z0-9-]", "", locator.partition(":")[0].lower())
    if candidate.startswith("working-tree"):
        scope = "working-tree"
    elif candidate.startswith("index"):
        scope = "index"
    elif candidate.startswith("history"):
        scope = "history"
    elif candidate.startswith("artifact"):
        scope = "artifact"
    elif candidate.startswith("fixture"):
        scope = "fixture"
    else:
        scope = "location"
    digest = hashlib.sha256(
        locator.encode("utf-8", errors="surrogatepass")
    ).hexdigest()[:16]
    return f"{scope or 'location'}#{digest}"


def searchable_text(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="ignore")
    if b"\0" in raw:
        text += "\n" + raw.replace(b"\0", b"").decode("utf-8", errors="ignore")
    return text


def matched_value_digest(match: re.Match[str]) -> str | None:
    for name, value in match.groupdict().items():
        if value is not None and name.startswith(
            ("password_", "secret_", "google_api_key")
        ):
            return hashlib.sha256(value.encode("utf-8")).hexdigest()
    return None


def scan_bytes(locator: str, raw: bytes) -> None:
    if len(raw) > MAX_CONTENT_SIZE:
        coverage_errors.add(f"oversized content was not scanned: {safe_locator(locator)}")
        return
    text = searchable_text(raw)
    matches = {
        label: list(pattern.finditer(text)) for label, pattern in PATTERNS.items()
    }
    specific_spans = [
        match.span()
        for label, label_matches in matches.items()
        if label not in FALLBACK_ASSIGNMENT_LABELS
        for match in label_matches
    ]
    for label, label_matches in matches.items():
        for match in label_matches:
            if label in FALLBACK_ASSIGNMENT_LABELS and any(
                match.start() <= start and end <= match.end()
                for start, end in specific_spans
            ):
                continue
            value_digest = matched_value_digest(match)
            classification = CLASSIFIED_VALUE_DIGESTS.get(value_digest or "")
            if classification:
                classifications.add((safe_locator(locator), classification))
                continue
            findings.add((safe_locator(locator), label))


def git_output(
    arguments: list[str], *, root: Path = ROOT, input_text: str | None = None
) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        input=input_text,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git command failed: {' '.join(arguments)}")
    return result.stdout


def git_bytes(arguments: list[str], *, root: Path = ROOT) -> bytes:
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git command failed: {' '.join(arguments)}")
    return result.stdout


def split_nul_records(raw: bytes) -> list[bytes]:
    if not raw:
        return []
    if not raw.endswith(b"\0"):
        raise RuntimeError("NUL-delimited repository enumeration was incomplete")
    return raw[:-1].split(b"\0")


def scan_working_tree(root: Path = ROOT) -> None:
    candidate_output = git_bytes(
        ["ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        root=root,
    )
    for relative_raw in split_nul_records(candidate_output):
        relative_text = os.fsdecode(relative_raw)
        scan_bytes(f"working-tree-path:{relative_text}", relative_raw)
        relative = Path(relative_text)
        if relative.is_absolute() or ".." in relative.parts:
            coverage_errors.add("unsafe repository path was not scanned")
            continue
        path = root / relative
        if path.is_symlink():
            scan_bytes(
                f"working-tree:{relative.as_posix()}",
                os.readlink(path).encode("utf-8", errors="surrogatepass"),
            )
        elif path.is_file():
            try:
                scan_bytes(f"working-tree:{relative.as_posix()}", path.read_bytes())
            except OSError:
                coverage_errors.add(
                    "unreadable repository file: "
                    + safe_locator(f"working-tree:{relative.as_posix()}")
                )
        else:
            coverage_errors.add(
                "repository entry is unavailable: "
                + safe_locator(f"working-tree:{relative.as_posix()}")
            )


def scan_index(root: Path = ROOT) -> None:
    """Scan every staged index path and blob, including uncommitted content."""
    entries = git_bytes(["ls-files", "--stage", "-z"], root=root)
    for entry in split_nul_records(entries):
        try:
            metadata, relative_raw = entry.split(b"\t", 1)
            mode, object_id_raw, stage = metadata.split(b" ")
        except ValueError:
            coverage_errors.add("Git index entry metadata could not be parsed")
            continue
        relative_text = os.fsdecode(relative_raw)
        scan_bytes(f"index-path:{relative_text}", relative_raw)
        if stage not in {b"0", b"1", b"2", b"3"}:
            coverage_errors.add("unsupported Git index stage was not scanned")
            continue
        if mode == b"160000":
            # A gitlink records only an object ID; its publishable path was scanned.
            continue
        object_id = object_id_raw.decode("ascii", errors="strict")
        locator = f"index:{object_id}:{relative_text}"
        result = subprocess.run(
            ["git", "cat-file", "blob", object_id],
            cwd=root,
            check=False,
            capture_output=True,
        )
        if result.returncode != 0:
            coverage_errors.add(f"unreadable Git index blob: {safe_locator(locator)}")
            continue
        scan_bytes(locator, result.stdout)


def split_ref_records(raw: bytes) -> list[bytes]:
    """Parse for-each-ref records terminated by NUL plus Git's format newline."""
    if not raw:
        return []
    delimiter = b"\0\n"
    if not raw.endswith(delimiter):
        raise RuntimeError("NUL-delimited Git ref enumeration was incomplete")
    return raw[: -len(delimiter)].split(delimiter)


def scan_refs(root: Path = ROOT) -> None:
    ref_output = git_bytes(["for-each-ref", "--format=%(refname)%00"], root=root)
    for ref_raw in split_ref_records(ref_output):
        scan_bytes("history-ref:" + os.fsdecode(ref_raw), ref_raw)


def scan_history(root: Path = ROOT) -> None:
    scan_refs(root)
    if git_output(["rev-parse", "--is-shallow-repository"], root=root).strip() == "true":
        coverage_errors.add("full Git history is unavailable in a shallow checkout")
        return

    object_ids = list(
        dict.fromkeys(
            git_output(
                ["rev-list", "--objects", "--all", "--no-object-names"],
                root=root,
            ).splitlines()
        )
    )

    if not object_ids:
        coverage_errors.add("Git history contains no reachable objects")
        return

    checks = git_output(
        ["cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)"],
        root=root,
        input_text="".join(f"{object_id}\n" for object_id in object_ids),
    )
    for line in checks.splitlines():
        parts = line.split()
        if len(parts) != 3:
            coverage_errors.add("Git object metadata could not be parsed")
            continue
        object_id, object_type, size_text = parts
        if object_type not in {"blob", "commit", "tag", "tree"}:
            coverage_errors.add("unsupported reachable Git object type was not scanned")
            continue
        try:
            size = int(size_text)
        except ValueError:
            coverage_errors.add("Git blob size could not be parsed")
            continue
        locator = f"history-{object_type}:{object_id}"
        if size > MAX_CONTENT_SIZE:
            coverage_errors.add(
                f"oversized history object was not scanned: {safe_locator(locator)}"
            )
            continue
        result = subprocess.run(
            ["git", "cat-file", object_type, object_id],
            cwd=root,
            check=False,
            capture_output=True,
        )
        if result.returncode != 0:
            coverage_errors.add(f"unreadable history object: {safe_locator(locator)}")
            continue
        scan_bytes(locator, result.stdout)


def scan_zip_archive(archive: zipfile.ZipFile, locator: str) -> None:
    scan_bytes(f"{locator}-comment", archive.comment)
    for entry in archive.infolist():
        entry_locator = f"{locator}-entry:{entry.filename}"
        scan_bytes(
            f"{entry_locator}-name",
            entry.filename.encode("utf-8", errors="surrogatepass"),
        )
        scan_bytes(f"{entry_locator}-comment", entry.comment)
        scan_bytes(f"{entry_locator}-extra", entry.extra)
        if entry.is_dir():
            continue
        if entry.file_size > MAX_CONTENT_SIZE:
            coverage_errors.add(
                "oversized artifact entry was not scanned: "
                + safe_locator(entry_locator)
            )
            continue
        try:
            scan_bytes(entry_locator, archive.read(entry))
        except (OSError, RuntimeError, zipfile.BadZipFile):
            coverage_errors.add(
                f"unreadable artifact entry: {safe_locator(entry_locator)}"
            )


def scan_artifact(path_text: str) -> None:
    scan_bytes("artifact-path:" + path_text, os.fsencode(path_text))
    candidate = Path(path_text)
    path = candidate if candidate.is_absolute() else Path.cwd() / candidate
    try:
        resolved = path.resolve(strict=True)
    except OSError:
        coverage_errors.add(f"artifact is unavailable: {safe_locator(path_text)}")
        return
    locator = f"artifact:{path_text}"
    if not resolved.is_file():
        coverage_errors.add(f"artifact is not a file: {safe_locator(path_text)}")
        return

    if zipfile.is_zipfile(resolved):
        try:
            with zipfile.ZipFile(resolved) as archive:
                scan_zip_archive(archive, locator)
        except (OSError, zipfile.BadZipFile):
            coverage_errors.add(f"artifact archive could not be read: {safe_locator(path_text)}")
        return

    try:
        scan_bytes(locator, resolved.read_bytes())
    except OSError:
        coverage_errors.add(f"artifact could not be read: {safe_locator(path_text)}")


def run_self_test() -> None:
    synthetic_fixtures = {
        "private key": "-----BEGIN " + "PRIVATE KEY-----",
        "JWT-like token": "eyJ" + "A" * 24 + "." + "B" * 24 + "." + "C" * 16,
        "Google API key": "AIza" + "D" * 35,
        "GitHub token": "ghp_" + "E" * 36,
        "AWS access key": "AKIA" + "F" * 16,
        "hard-coded secret assignment": "client_" + "secret=" + "G" * 32,
    }
    saved = (set(findings), set(classifications), set(coverage_errors))
    findings.clear()
    classifications.clear()
    coverage_errors.clear()
    try:
        for index, (expected_label, fixture) in enumerate(synthetic_fixtures.items()):
            scan_bytes(f"fixture-content:{index}", fixture.encode())
            if not any(label == expected_label for _, label in findings):
                raise RuntimeError(f"secret scanner self-test missed {expected_label}")

        records = split_nul_records(b"normal\0odd\nname\0")
        if records != [b"normal", b"odd\nname"]:
            raise RuntimeError("secret scanner self-test failed NUL path parsing")

        path_secret = "ghp_" + "H" * 36
        unusual_path = "odd\n" + path_secret
        scan_bytes("fixture-path:" + unusual_path, unusual_path.encode())
        scan_bytes("history-commit:synthetic", ("release " + path_secret).encode())
        scan_bytes("history-tag:synthetic", ("tag " + path_secret).encode())

        archive_buffer = io.BytesIO()
        with zipfile.ZipFile(archive_buffer, "w") as archive:
            archive.comment = ("archive " + path_secret).encode()
            archive.writestr("assets/" + path_secret, b"safe content")
        archive_buffer.seek(0)
        with zipfile.ZipFile(archive_buffer) as archive:
            scan_zip_archive(archive, "fixture-artifact:synthetic")

        staged_token = "glpat-" + "I" * 24
        commit_token = "ghp_" + "J" * 36
        tag_token = "AKIA" + "K" * 16
        ref_token = "xoxb-" + "L" * 24
        with tempfile.TemporaryDirectory(prefix="pampan-secret-scan-") as temporary:
            repository = Path(temporary)

            def fixture_git(arguments: list[str]) -> bytes:
                result = subprocess.run(
                    ["git", *arguments],
                    cwd=repository,
                    check=False,
                    capture_output=True,
                )
                if result.returncode != 0:
                    raise RuntimeError(
                        "secret scanner end-to-end fixture setup failed"
                    )
                return result.stdout

            fixture_git(["init", "--quiet"])
            fixture_git(["config", "user.name", "Secret Scanner Fixture"])
            fixture_git(["config", "user.email", "scanner@example.invalid"])
            (repository / "history.txt").write_text("safe history\n")
            fixture_git(["add", "history.txt"])
            fixture_git(["commit", "--quiet", "-m", "release " + commit_token])
            fixture_git(["tag", "-a", "regression", "-m", "tag " + tag_token])
            fixture_git(["branch", ref_token])
            (repository / "staged.txt").write_text(staged_token + "\n")
            fixture_git(["add", "staged.txt"])
            staged_object = fixture_git(["rev-parse", ":staged.txt"]).decode().strip()
            (repository / "staged.txt").write_text("safe working tree\n")

            commit_object = fixture_git(["rev-parse", "HEAD"]).decode().strip()
            tag_object = fixture_git(
                ["rev-parse", "refs/tags/regression"]
            ).decode().strip()
            before_repository_scan = set(findings)
            scan_working_tree(repository)
            scan_index(repository)
            scan_history(repository)
            repository_findings = findings - before_repository_scan
            expected_repository_findings = {
                (safe_locator(f"index:{staged_object}:staged.txt"), "GitLab token"),
                (safe_locator(f"history-commit:{commit_object}"), "GitHub token"),
                (safe_locator(f"history-tag:{tag_object}"), "AWS access key"),
                (
                    safe_locator(f"history-ref:refs/heads/{ref_token}"),
                    "Slack token",
                ),
            }
            if not expected_repository_findings.issubset(repository_findings):
                raise RuntimeError(
                    "secret scanner end-to-end repository coverage regressed"
                )

        placeholder = "password" + "123"
        assignment_key = "pass" + "word"
        scan_bytes(
            "fixture-placeholder:approved",
            f'{assignment_key}: "{placeholder}"'.encode(),
        )
        scan_bytes(
            "fixture-placeholder:changed",
            f'{assignment_key}: "{placeholder}x"'.encode(),
        )
        if not any(label == "user-confirmed placeholder" for _, label in classifications):
            raise RuntimeError("secret scanner self-test missed approved classification")
        if not any(
            label == "hard-coded password assignment" for _, label in findings
        ):
            raise RuntimeError("secret scanner self-test classification was too broad")

        rendered = "\n".join(
            [f"{locator}: {label}" for locator, label in findings]
            + [f"{locator}: {label}" for locator, label in classifications]
            + sorted(coverage_errors)
        )
        for forbidden in [
            *synthetic_fixtures.values(),
            path_secret,
            unusual_path,
            placeholder,
            staged_token,
            commit_token,
            tag_token,
            ref_token,
        ]:
            if forbidden in rendered:
                raise RuntimeError("secret scanner self-test detected unredacted output")
    finally:
        findings.clear()
        findings.update(saved[0])
        classifications.clear()
        classifications.update(saved[1])
        coverage_errors.clear()
        coverage_errors.update(saved[2])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-history",
        action="store_true",
        help="scan publishable working-tree content without Git history",
    )
    parser.add_argument(
        "--artifact",
        action="append",
        default=[],
        metavar="PATH",
        help="also scan a generated file or archive; may be repeated",
    )
    parser.add_argument(
        "--artifact-only",
        action="store_true",
        help="scan only requested artifacts, without the working tree or history",
    )
    parser.add_argument(
        "--self-test-only",
        action="store_true",
        help="run synthetic redaction/detection regression fixtures only",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.artifact_only and not args.artifact:
        print("Secret scan could not complete safely: --artifact-only requires --artifact")
        return 2
    try:
        run_self_test()
        if args.self_test_only:
            print("Secret scanner self-test passed.")
            return 0
        if not args.artifact_only:
            scan_working_tree()
            scan_index()
            if not args.no_history:
                scan_history()
        for artifact in args.artifact:
            scan_artifact(artifact)
    except RuntimeError as error:
        print(f"Secret scan could not complete safely: {error}")
        return 2

    if coverage_errors:
        print("Secret scan coverage failed (content values redacted):")
        for error in sorted(coverage_errors):
            print(f"- {error}")
    if findings:
        print("Secret scan found credential-like content (values redacted):")
        for locator, label in sorted(findings):
            print(f"- {locator}: possible {label}")
    if coverage_errors or findings:
        return 1

    if classifications:
        print("Classified publishable client configuration (values redacted):")
        for locator, label in sorted(classifications):
            print(f"- {locator}: {label}")

    if args.artifact_only:
        scopes = "requested artifacts"
    else:
        scopes = "publishable working-tree and index content"
        if not args.no_history:
            scopes += ", full Git history"
        if args.artifact:
            scopes += ", and requested artifacts"
    print(f"Secret scan passed for {scopes}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
