# PamPan — pantry assistant
<img src=https://github.com/user-attachments/assets/eba34415-3003-46b8-9367-fc4ae7797a2e width=32>
PamPan is a Flutter pantry-management application intended to help reduce food waste. It was originally written for the IEEE Students Day competition in 2024.

> **Repository state:** `PAMPAN-NATIVE-REWRITE` / I1E and the larger Android foundation I1 are **complete / PASS** only for exact state `I1E@660a5e39619d036d6b9228a97a18b2e036c44afd/tree-bcfdba270ae6938528de1af63f06244aec9331dc/run-30023752408/protected-82e0e3377b9f302b853ed7c5f3e0d1b0dc4cb5af269a628b5224722f775fb923` under the approved revised static-only CI policy. The exact run and both configured final gates passed. All 20 protected Android behavior files were byte-identical to the accepted I1B materialization, so physical connected-test, offline-launch, and TalkBack evidence carries by equivalence, not retest; future protected drift requires a freshly approved phone gate. Hosted-emulator acceptance remains withdrawn/superseded, never retroactively passed. I1C remains **failed / BLOCKED historical evidence**, and I1D remains **complete / PASS for Diagnostic PASS only**. The full rewrite is not complete: Android remains the only active native application, `apps/ios/` is dormant, `pam_pan/` remains unchanged from `0512f84`, and I2–I9 remain inactive pending fresh approval.
>
> **Public repository:** treat every repository path, commit, branch, pull-request diff, CI log, test fixture, example, generated artifact, and release artifact as public. Never add secrets, private signing material, or live credentials. Read [SECURITY.md](SECURITY.md) and the [public-repository security boundary](docs/reference/public-repository-security.html) before configuration, integration, CI, or release work.

## Documentation and agent entrypoints

- Browser portal: [index.html](index.html)
- Agent instructions: [AGENTS.md](AGENTS.md)
- Documentation guide: [docs/README.md](docs/README.md)
- Active-state manifest: [docs/manifest.yaml](docs/manifest.yaml)
- Completed reverse-engineering specification: [PAMPAN-REWRITE-SPEC](docs/planning/completed/pampan-rewrite-spec.html)
- Active native rewrite specification: [PAMPAN-NATIVE-REWRITE](docs/planning/active/pampan-native-rewrite.html)
- Active native rewrite roadmap: [I1–I9 roadmap](docs/planning/active/pampan-native-rewrite-roadmap.html)
- Completed I1E record: [static-only CI acceptance transition and hosted-emulator removal](docs/planning/completed/pampan-native-rewrite-i1e.html)
- Historical I1C record: [failed single authorized hosted-emulator run](docs/planning/completed/pampan-native-rewrite-i1c.html)
- Completed I1D record: [Diagnostic PASS with sanitized emulator matrix](docs/planning/completed/pampan-native-rewrite-i1d.html)
- Completed I1B record: [physical-device verification and sanitized evidence](docs/planning/completed/pampan-native-rewrite-i1b.html)
- Completed I1B-R1 record: [dependency-verification metadata prerequisite](docs/planning/completed/pampan-native-rewrite-i1b-r1.html)
- Completed I1A record: [Android-only and public-repository transition](docs/planning/completed/pampan-native-rewrite-i1a.html)
- Current handover: [current.html](docs/handover/current.html)
- Security policy: [SECURITY.md](SECURITY.md)
- Public-repository security boundary: [docs/reference/public-repository-security.html](docs/reference/public-repository-security.html)

### Legacy README claims (unverified)
- CRUD operations on food items for an appwrite and a scrapped sqlite database.
- Automatic filling of item details using barcodes or Gemini vision AI.
- Automatic reminder notifications when items are near-expiry.
- Chatbot integration (WIP. Recommends recipies using near-expiry items).
- Calendar view of pantry's expiry dates.
- (Incomplete) Map view of nearest food shelters.

### Screenshots
<img src=https://github.com/user-attachments/assets/76e3e5c4-4773-43d9-a0f6-de2fde445651 width=250>
<img src=https://github.com/user-attachments/assets/e4d4dabc-d1a8-479c-9fc4-4804e0dae289 width=250>

### Observed legacy technology (not a rewrite decision)
- Frontend: Flutter
- Backend: Appwrite and Google Firebase (for Gemini AI)
- Programming language: Dart
