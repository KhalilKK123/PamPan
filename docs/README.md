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

`PAMPAN-NATIVE-REWRITE` / I1A, [I1B-R1](planning/completed/pampan-native-rewrite-i1b-r1.html), [physical-device I1B](planning/completed/pampan-native-rewrite-i1b.html), and [I1D](planning/completed/pampan-native-rewrite-i1d.html) are complete / PASS only for their recorded exact states and outcomes. I1D passed its bounded Diagnostic PASS objective only; Recovery PASS was not achieved. [I1C](planning/active/pampan-native-rewrite-i1c.html) remains BLOCKED after its failed single authorized run. Android is the only active native application; the existing iOS foundation is preserved dormant and excluded from active implementation and gates. The larger native rewrite I1 remains BLOCKED pending same-state emulator launch, connected testing, required TalkBack/accessibility, and complete exit evidence. I2–I9 remain inactive and require fresh approval. Read the [living specification](planning/active/pampan-native-rewrite.html), [roadmap](planning/active/pampan-native-rewrite-roadmap.html), completed I1D record, I1C blocked predecessor, manifest, [current handover](handover/current.html), and [public-repository security boundary](reference/public-repository-security.html) before work. This repository is public: secret safety applies to source, docs, tests, fixtures, examples, CI configuration and output, generated/release artifacts, local configuration, signing material, and Git history. Regenerate navigation with `python3 scripts/update-doc-navigation.py` and validate with `python3 scripts/check-docs.py`.
