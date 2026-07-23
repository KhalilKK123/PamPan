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

`PAMPAN-NATIVE-REWRITE` / [I1E](planning/completed/pampan-native-rewrite-i1e.html) and the larger Android foundation I1 are complete / PASS only for their exact recorded state under the approved revised static-only policy. The exact run and both configured final gates passed. All 20 protected Android behavior files were byte-identical to the accepted [physical-device I1B](planning/completed/pampan-native-rewrite-i1b.html) materialization, so connected-test, offline-launch, and TalkBack evidence carries by equivalence, not retest; future protected drift requires a freshly approved phone gate. [I1C](planning/completed/pampan-native-rewrite-i1c.html) remains failed / BLOCKED historical evidence, and [I1D](planning/completed/pampan-native-rewrite-i1d.html) remains Diagnostic PASS only. Hosted-emulator acceptance is withdrawn/superseded, never retroactively passed. The full rewrite is not complete; I2–I9 remain inactive and require fresh approval. Read the [living specification](planning/active/pampan-native-rewrite.html), [roadmap](planning/active/pampan-native-rewrite-roadmap.html), completed I1E record, manifest, [current handover](handover/current.html), and [public-repository security boundary](reference/public-repository-security.html) before work. This repository is public: secret safety applies to source, docs, tests, fixtures, examples, CI configuration and output, generated/release artifacts, local configuration, signing material, and Git history. Regenerate navigation with `python3 scripts/update-doc-navigation.py` and validate with `python3 scripts/check-docs.py`.
