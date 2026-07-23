# Agent instructions — PamPan

Start substantial work by reading `README.md`, `docs/README.md`, `docs/manifest.yaml`, `docs/handover/current.html`, and the active planning files identified by the manifest.

## Documentation ownership

- `docs/reference/` records verified current behavior, operating policy, and remaining evidence limits.
- `docs/planning/active/` is the authority for approved future work.
- `docs/handover/current.html` is a resume aid, not architecture authority.
- Run `python3 scripts/update-doc-navigation.py` after durable documentation tree changes, then `python3 scripts/check-docs.py`.

## Active constraint

`PAMPAN-REWRITE-SPEC` / `I1` is complete with a PASS for its documented static-analysis exit gate and is preserved in `docs/planning/completed/` as durable rewrite input. `PAMPAN-NATIVE-REWRITE` / `I1E` and the larger Android foundation `I1` are **complete / PASS** only for exact state `I1E@660a5e39619d036d6b9228a97a18b2e036c44afd/tree-bcfdba270ae6938528de1af63f06244aec9331dc/run-30023752408/protected-82e0e3377b9f302b853ed7c5f3e0d1b0dc4cb5af269a628b5224722f775fb923` under the revised static-only policy. GitHub Actions covers static analysis, unit tests, builds/assembly, dependency verification/locks, native audits, APK/repository security, documentation, and scope invariants only. Hosted emulator/system-image/AVD/ADB/connected/runtime/TalkBack gates are withdrawn and superseded, never retroactively passed.

A physical phone is the sole runtime, connected-test, and TalkBack surface. I1B evidence carries to the exact I1E state through verified byte identity of all 20 protected Android behavior files; this is equivalence-based acceptance, not a retest. Any future protected drift requires a freshly and explicitly approved phone gate. I1C remains failed / BLOCKED historical evidence; I1D remains complete / PASS for Diagnostic PASS only. Do not mark the full rewrite complete: I2–I9 remain inactive and require fresh approval.

Android is the only active native application. Preserve `apps/ios/` as dormant; do not implement, build, test, verify, release, delete, or rewrite iOS work unless Rein gives fresh explicit approval. CI and validators must remain Android-only. I2–I9 remain inactive and require fresh approval. Do not add product behavior, choose beyond the approved target stack, invent server contracts, resolve historical blockers without evidence, or change `pam_pan/` from `0512f84`.

This is a public repository. Read `SECURITY.md` and `docs/reference/public-repository-security.html` before configuration, integration, CI, fixture, artifact, or release work. Never place secrets, credentials, private keys, signing material, private endpoints, or sensitive user data in source, docs, tests, fixtures, examples, logs, CI output, artifacts, local configuration intended for commit, or Git history. Use redacted evidence when auditing; do not reproduce suspected values. A suspected disclosure is a stop condition requiring private escalation and credential revocation or rotation outside repository history before cleanup claims.

Code and executable configuration outrank docs for implemented behavior. Record uncertainty with source paths and confidence; do not convert inference into fact.
