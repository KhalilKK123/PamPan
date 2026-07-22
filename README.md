# PamPan — pantry assistant
<img src=https://github.com/user-attachments/assets/eba34415-3003-46b8-9367-fc4ae7797a2e width=32>
PamPan is a Flutter pantry-management application intended to help reduce food waste. It was originally written for the IEEE Students Day competition in 2024.

> **Repository state:** `PAMPAN-NATIVE-REWRITE` / I1A is implemented, independently verified and reviewed, and **complete / PASS** for state `I1A@0512f84/worktree-2d120810/index-e3b0c442/untracked-37221eae`. Android is the only active native application; `apps/ios/` is preserved dormant and excluded from implementation, build, test, CI, verification, and release gates unless fresh approval reactivates it. The larger native rewrite I1 remains **BLOCKED / pending verification**, not complete or PASS, until Android emulator launch, connected tests, TalkBack, and an actual GitHub Actions run are evidenced. The legacy Flutter package remains unchanged from `0512f84`.
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
