#!/usr/bin/env python3
"""Assert the exact Android/JDK foundation toolchain."""

from pathlib import Path
import os
import re
import subprocess
import sys

sdk_root_text = os.environ.get("ANDROID_SDK_ROOT") or os.environ.get("ANDROID_HOME")
if not sdk_root_text:
    print("ANDROID_SDK_ROOT or ANDROID_HOME is required.")
    sys.exit(1)

sdk_root = Path(sdk_root_text)
expected_properties = {
    sdk_root / "cmdline-tools/latest/source.properties": ("Pkg.Revision", "19.0"),
    sdk_root / "platform-tools/source.properties": ("Pkg.Revision", "37.0.0"),
    sdk_root / "platforms/android-36/source.properties": ("Pkg.Revision", "2"),
    sdk_root / "build-tools/36.0.0/source.properties": ("Pkg.Revision", "36.0.0"),
    sdk_root / "emulator/source.properties": ("Pkg.Revision", "36.6.11"),
    sdk_root / "system-images/android-36/google_apis/x86_64/source.properties": (
        "Pkg.Revision",
        "7",
    ),
}

errors: list[str] = []
for path, (key, expected) in expected_properties.items():
    if not path.exists():
        errors.append(f"missing toolchain metadata: {path}")
        continue
    values = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            property_key, value = line.split("=", 1)
            values[property_key] = value
    if values.get(key) != expected:
        errors.append(f"{path}: expected {key}={expected}, got {values.get(key)!r}")

java_version = subprocess.run(
    ["java", "-version"], capture_output=True, text=True, check=False
)
java_output = java_version.stderr + java_version.stdout
if not re.search(r'openjdk version "17\.0\.19(?:[+\"]|$)', java_output):
    errors.append("expected exact OpenJDK 17.0.19 runtime")

emulator_binary = sdk_root / "emulator/emulator"
if not emulator_binary.is_file() or not os.access(emulator_binary, os.X_OK):
    errors.append("Android emulator executable is missing or not executable")

if errors:
    print("Android toolchain check failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Android toolchain check passed: JDK 17.0.19, command-line tools 19.0, platform-tools 37.0.0, API 36 r2, build-tools 36.0.0, emulator 36.6.11, system image r7.")
