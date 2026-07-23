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
./gradlew connectedDebugAndroidTest
```

Open this directory in Android Studio for local inspection. The application declares no runtime permission and contains no service SDK.

The strict offline lint/unit/assembly/release-lock command passed for the recorded I1A state. Physical-device I1B subsequently passed strict connected instrumentation, offline launch, and all approved manual foundation/TalkBack checks for its exact recorded state. I1D completed / PASS for its bounded Diagnostic PASS objective: its sanitized matrix and digest matched, but the emulator exited before ADB registration, API 36 boot was not established, and the connected test was not reached. Recovery PASS was not achieved. The larger native rewrite I1 remains blocked pending same-state emulator launch, connected testing, required TalkBack/accessibility, and complete exit evidence.

Future local Android SDK paths belong in ignored `local.properties`. Future service values must use ignored local configuration or CI secrets and must never include a Supabase service-role key.

The repository is public. Do not place credentials, signing keys, private endpoints, sensitive fixtures, or live user data in source, resources, manifests, tests, logs, build outputs, examples, or Git history. Public client configuration must be deliberately classified and documented before use; “client-side” does not by itself make a value safe to publish. See `../../SECURITY.md`.
