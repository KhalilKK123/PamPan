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

The strict offline lint/unit/assembly/release-lock command passed for the recorded I1A state. Physical-device I1B subsequently passed strict connected instrumentation, offline launch, and all approved manual foundation/TalkBack checks for its exact recorded state. Successful API 36 emulator evidence and a successful actual GitHub Actions run remain required before the larger native rewrite I1 can pass; approved I1C has not yet supplied either result.

Future local Android SDK paths belong in ignored `local.properties`. Future service values must use ignored local configuration or CI secrets and must never include a Supabase service-role key.

The repository is public. Do not place credentials, signing keys, private endpoints, sensitive fixtures, or live user data in source, resources, manifests, tests, logs, build outputs, examples, or Git history. Public client configuration must be deliberately classified and documented before use; “client-side” does not by itself make a value safe to publish. See `../../SECURITY.md`.
