# PamPan documentation

Open [the browser portal](../index.html) for the complete documentation tree. `docs/manifest.yaml` is the canonical catalog and active-work registry.

| Location | Authority |
| --- | --- |
| `reference/` | Verified present behavior and operating facts |
| `architecture/` | Verified current boundaries and data flow |
| `planning/active/` | Approved future work and active increment plans |
| `planning/completed/` | Preserved completed execution records |
| `handover/` | Session resume state and changelog |
| `notes/`, `reviews/`, `reports/`, `archive/` | Temporary, assessment, analytical, and historical material respectively |
| `templates/` | Reusable document skeletons; not project truth |

`PAMPAN-NATIVE-REWRITE` / I1A is [complete / PASS](planning/completed/pampan-native-rewrite-i1a.html) for its recorded implementation state. [I1B is approved / not started](planning/active/pampan-native-rewrite-i1b.html) for physical-device connected tests, offline launch, and user-observed TalkBack evidence. Android is the only active native application; the existing iOS foundation is preserved dormant and excluded from active implementation and gates. The larger native rewrite I1 remains BLOCKED: a local I1B PASS would still leave successful actual-CI and emulator evidence for a separate approved increment. I2–I9 remain inactive. Read the [living specification](planning/active/pampan-native-rewrite.html), [roadmap](planning/active/pampan-native-rewrite-roadmap.html), manifest, [current handover](handover/current.html), and [public-repository security boundary](reference/public-repository-security.html) before work. This repository is public: secret safety applies to source, docs, tests, fixtures, examples, CI configuration and output, generated/release artifacts, local configuration, signing material, and Git history. Regenerate navigation with `python3 scripts/update-doc-navigation.py` and validate with `python3 scripts/check-docs.py`.
