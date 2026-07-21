# Agent instructions — PamPan

Start substantial work by reading `README.md`, `docs/README.md`, `docs/manifest.yaml`, `docs/handover/current.html`, and the active planning files identified by the manifest.

## Documentation ownership

- `docs/reference/` records verified current behavior, operating policy, and remaining evidence limits.
- `docs/planning/active/` is the authority for approved future work.
- `docs/handover/current.html` is a resume aid, not architecture authority.
- Run `python3 scripts/update-doc-navigation.py` after durable documentation tree changes, then `python3 scripts/check-docs.py`.

## Active constraint

`PAMPAN-REWRITE-SPEC` / `I1` is complete with a PASS for its documented static-analysis exit gate and is preserved in `docs/planning/completed/` as durable rewrite input. `PAMPAN-NATIVE-REWRITE` / `I1A` is independently verified/reviewed and **complete / PASS** only for its recorded implementation state. Commit `e14ddad236b78d20708de71a09a489c98c30dd4f` captures that foundation and, at I1B activation, is local and not yet pushed. `PAMPAN-NATIVE-REWRITE` / `I1B` is the approved active increment for exact-state Android runtime, TalkBack, and actual-CI evidence closure. The larger I1 remains **BLOCKED / pending verification**; do not mark it or the full rewrite complete or PASS until every I1B exit-gate item is evidenced for one executable state.

Android is the only active native application. Preserve `apps/ios/` as dormant; do not implement, build, test, verify, release, delete, or rewrite iOS work unless Rein gives fresh explicit approval. CI and validators must remain Android-only. I2–I9 remain inactive and require fresh approval. Do not add product behavior, choose beyond the approved target stack, invent server contracts, resolve historical blockers without evidence, or change `pam_pan/` from `0512f84`.

This is a public repository. Read `SECURITY.md` and `docs/reference/public-repository-security.html` before configuration, integration, CI, fixture, artifact, or release work. Never place secrets, credentials, private keys, signing material, private endpoints, or sensitive user data in source, docs, tests, fixtures, examples, logs, CI output, artifacts, local configuration intended for commit, or Git history. Use redacted evidence when auditing; do not reproduce suspected values. A suspected disclosure is a stop condition requiring private escalation and credential revocation or rotation outside repository history before cleanup claims.

Code and executable configuration outrank docs for implemented behavior. Record uncertainty with source paths and confidence; do not convert inference into fact.
