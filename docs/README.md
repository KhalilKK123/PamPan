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

`PAMPAN-NATIVE-REWRITE` / [I1E](planning/active/pampan-native-rewrite-i1e.html) is the sole active successor and is approved / pending implementation. GitHub Actions acceptance is static-only; runtime launch, connected testing, and TalkBack belong exclusively to a freshly approved physical-phone gate. Completed [physical-device I1B](planning/completed/pampan-native-rewrite-i1b.html) evidence may carry forward only through verified protected-byte identity; this is equivalence-based acceptance, not a retest. [I1C](planning/completed/pampan-native-rewrite-i1c.html) is failed / BLOCKED historical evidence, and [I1D](planning/completed/pampan-native-rewrite-i1d.html) remains complete / PASS for Diagnostic PASS only. Hosted-emulator verification is withdrawn and superseded, never retroactively passed. Larger I1 remains BLOCKED until I1E implementation, one exact successful static-only GitHub Actions run, protected equivalence, and configured final gates pass. I2–I9 remain inactive. Read the active I1E plan, [living specification](planning/active/pampan-native-rewrite.html), [roadmap](planning/active/pampan-native-rewrite-roadmap.html), manifest, [current handover](handover/current.html), and [public-repository security boundary](reference/public-repository-security.html) before work. This repository is public: secret safety applies to source, docs, tests, fixtures, examples, CI configuration and output, generated/release artifacts, local configuration, signing material, and Git history. Regenerate navigation with `python3 scripts/update-doc-navigation.py` and validate with `python3 scripts/check-docs.py`.
