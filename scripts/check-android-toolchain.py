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
    sdk_root / "cmdline-tools/latest/source.properties": (
        "Android command-line tools",
        "Pkg.Revision",
        "19.0",
    ),
    sdk_root / "platform-tools/source.properties": (
        "Android platform tools",
        "Pkg.Revision",
        "37.0.0",
    ),
    sdk_root / "platforms/android-36/source.properties": (
        "Android API 36 platform",
        "Pkg.Revision",
        "2",
    ),
    sdk_root / "build-tools/36.0.0/source.properties": (
        "Android Build Tools 36.0.0",
        "Pkg.Revision",
        "36.0.0",
    ),
}

errors: list[str] = []
for path, (label, key, expected) in expected_properties.items():
    if not path.exists():
        errors.append(f"{label} metadata is missing")
        continue
    values = {}
    try:
        metadata_lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        errors.append(f"{label} metadata could not be read")
        continue
    for line in metadata_lines:
        if "=" in line and not line.startswith("#"):
            property_key, value = line.split("=", 1)
            values[property_key] = value
    if values.get(key) != expected:
        errors.append(
            f"{label} metadata does not match the required {key}={expected}"
        )

try:
    java_version = subprocess.run(
        ["java", "-version"], capture_output=True, text=True, check=False
    )
except OSError:
    errors.append("OpenJDK runtime is missing or could not execute")
else:
    java_output = java_version.stderr + java_version.stdout
    if not re.search(r'openjdk version "17\.0\.19(?:[+\"]|$)', java_output):
        errors.append("expected exact OpenJDK 17.0.19 runtime")

if errors:
    print("Android toolchain check failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Android toolchain check passed: JDK 17.0.19, command-line tools 19.0, platform-tools 37.0.0, API 36 r2, build-tools 36.0.0.")
