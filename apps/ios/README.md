# PamPan for iOS

Native SwiftUI foundation targeting iOS 17 or newer, preserved as dormant historical work.

## Dormant scope

Android is the only active native application. Do not implement, build, test, verify, release, delete, or rewrite this iOS foundation without fresh explicit approval. The requirements and command below are retained only as historical foundation documentation; they are not an active CI or completion gate.

## Requirements

- macOS with Xcode 16.4
- iOS 18.5 Simulator runtime (the exact available simulator identifier may differ)

## Verify

```bash
xcodebuild \
  -project PamPan.xcodeproj \
  -scheme PamPan \
  -configuration Debug \
  -destination 'platform=iOS Simulator,name=iPhone 16 Pro,OS=18.5' \
  test \
  CODE_SIGNING_ALLOWED=NO
```

The historical dual-platform I1 gate required an offline launch and VoiceOver check. Completed I1A removed iOS from active gates without changing the dormant executable project.

No runtime service configuration exists in the preserved foundation. Do not add local or production values while iOS is dormant. This repository is public; secrets and signing material must never be committed, logged, documented, or compiled into an artifact. See `../../SECURITY.md`.
