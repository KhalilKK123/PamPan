# Security policy

PamPan is a public repository. Assume that every path, commit, branch, pull-request diff, issue attachment, CI log, test report, cache, generated artifact, and release artifact can become public and permanent.

## Repository safety boundary

Do not commit, paste, print, upload, or package:

- passwords, access tokens, API secrets, service-role keys, private keys, certificates, signing keystores, provisioning credentials, or recovery material;
- private service endpoints, internal infrastructure details, sensitive environment values, or credentials copied from the legacy application;
- production or personal data in tests, fixtures, screenshots, crash reports, analytics, examples, seed data, or documentation;
- local SDK paths, machine-specific configuration, editor state, debug dumps, or secret-bearing build outputs.

Client-side configuration is not automatically safe. A value may be checked in only after it is deliberately classified as publishable, is constrained by server-side authorization and least privilege, and is represented without accompanying secret material. Supabase service-role keys and third-party provider credentials are never client configuration.

Use ignored local files or the CI platform's protected secret storage for necessary private values. Commit only redacted templates and synthetic fixtures. Keep logs, tests, examples, documentation, and failure messages redacted.

## Review and response

Secret-safety review must cover the working tree, tracked and relevant untracked files, dormant and legacy directories, Git history, CI configuration and output, generated Android artifacts, examples, fixtures, local configuration patterns, and signing material. Report only file paths, categories, fingerprints, or other redacted evidence; do not reproduce a suspected value in a command, log, issue, commit message, or document.

If a suspected disclosure is found:

1. Stop publishing, releasing, or copying the affected material.
2. Do not open a public issue or paste the value into chat or documentation.
3. Notify the maintainer privately, using GitHub private vulnerability reporting when available.
4. Revoke or rotate the credential at its provider before treating repository cleanup as sufficient.
5. Preserve only redacted evidence and verify the working tree, history, CI logs, caches, and artifacts again.

Deleting a file or commit does not invalidate a disclosed credential. History rewriting, credential rotation, provider changes, and deletion of remote artifacts require separate explicit authorization and coordinated handling.

## Current project scope

Android is the only active native application. `apps/ios/` is preserved as dormant and must still be included in redacted repository-safety review even though it is outside implementation, build, test, verification, and release gates. The frozen legacy package at `pam_pan/` must remain unchanged from `0512f84`, but its presence does not exempt it or its Git history from redacted disclosure review.

See `docs/reference/public-repository-security.html` for the durable agent-facing operating boundary and current evidence status.

## Current enforcement

I1A completed with independent verification and review. The repository scanner covers publishable working-tree paths and content, all staged index paths and blobs, reachable Git blob/commit/tag/tree objects, Git ref names, and requested Android APK path/archive metadata/entry metadata/content. Findings and classifications use redacted opaque locators; approved placeholder and publishable legacy Google client configuration classifications are keyed by exact-value digest without reproducing values. CI runs repository/history/index/ref scanning and scans the generated APK. Ignore rules cover local secret, signing, and provider configuration patterns.

This evidence applies only to the recorded I1A implementation state. A later content, scanner, CI, packaging, or classification change requires fresh same-state verification. A passing scan does not waive the incident-response rules above.
