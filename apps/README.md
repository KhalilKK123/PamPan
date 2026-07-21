# Native applications

Android is the only active native application:

- `android/`: active Kotlin and Jetpack Compose application, Android API 26 or newer.
- `ios/`: preserved dormant Swift/SwiftUI foundation. Do not implement, build, test, verify, release, delete, or rewrite it without fresh explicit approval.

I1A is complete / PASS: active CI, validation, verification, and release planning are Android-only while iOS files remain preserved. I1A added no product behavior. Shared assets under `../contracts/` are non-executable; future active contract work targets Android unless scope is explicitly changed.

This repository is public. Never commit credentials, signing material, private service values, sensitive fixtures, or secret-bearing generated artifacts. See `../SECURITY.md` and `../docs/reference/public-repository-security.html`.
