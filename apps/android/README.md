# PamPan for Android

Native Kotlin and Jetpack Compose foundation targeting Android API 26 or newer.

Android is the only active native application. I1A is complete / PASS; iOS is outside Android implementation, CI, verification, and release gates.

## Pinned toolchain

- JDK 17
- Gradle 8.11.1 (wrapper)
- Android Gradle Plugin 8.10.1
- Kotlin 2.1.21
- compile/target SDK 36
- Android Build Tools 36.0.0

## Verify

```bash
./gradlew --offline --no-daemon --dependency-verification strict ktlintCheck lintDebug testDebugUnitTest assembleDebug :app:writeReleaseRuntimeLock
```

Open this directory in Android Studio for local inspection. The application declares no runtime permission and contains no service SDK.

I1E and the larger Android foundation I1 are complete / PASS only for their exact recorded state under the revised static-only CI policy. The exact static-only run and both configured final gates passed. All 20 protected Android behavior files were byte-identical to accepted physical-device I1B materialization, so connected-test, offline-launch, and TalkBack evidence carries by equivalence, not retest. Hosted-emulator acceptance remains withdrawn/superseded and was never retroactively passed.

A physical phone is the sole connected-test, runtime-launch, and TalkBack verification surface. Do not run `connectedDebugAndroidTest` or begin device work without a freshly and explicitly approved phone gate. Any future protected Android behavior drift requires new approved physical-device evidence.

Future local Android SDK paths belong in ignored `local.properties`. Future service values must use ignored local configuration or CI secrets and must never include a Supabase service-role key.

The repository is public. Do not place credentials, signing keys, private endpoints, sensitive fixtures, or live user data in source, resources, manifests, tests, logs, build outputs, examples, or Git history. Public client configuration must be deliberately classified and documented before use; “client-side” does not by itself make a value safe to publish. See `../../SECURITY.md`.
