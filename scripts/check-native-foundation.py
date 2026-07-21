#!/usr/bin/env python3
"""Validate the Android-only code boundaries of PAMPAN-NATIVE-REWRITE I1A."""

import argparse
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ANDROID_MANIFEST = ROOT / "apps/android/app/src/main/AndroidManifest.xml"
ANDROID_SOURCE = ROOT / "apps/android/app/src/main"

errors: list[str] = []
parser = argparse.ArgumentParser()
parser.add_argument(
    "--require-assembled-android",
    action="store_true",
    help="fail unless an assembled merged Android manifest can be audited",
)
args = parser.parse_args()

required = [
    ROOT / "apps/android/gradlew",
    ROOT / "apps/android/app/build.gradle.kts",
    ROOT / "contracts/README.md",
    ROOT / "supabase/README.md",
]
for path in required:
    if not path.exists():
        errors.append(f"missing required foundation path: {path.relative_to(ROOT)}")

if ANDROID_MANIFEST.exists():
    manifest = ANDROID_MANIFEST.read_text(encoding="utf-8")
    if "uses-permission" in manifest:
        errors.append("Android I1 manifest must not declare permissions")

android_namespace = "{http://schemas.android.com/apk/res/android}"
allowed_assembled_permissions = {
    "com.pampan.pampan.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION",
}
merged_manifests = list(
    (ROOT / "apps/android/app/build/intermediates").glob(
        "**/processDebugManifest/AndroidManifest.xml"
    )
)
if args.require_assembled_android and not merged_manifests:
    errors.append("assembled Android manifest is required but was not found")
for merged_manifest in merged_manifests:
    try:
        root = ET.parse(merged_manifest).getroot()
    except ET.ParseError as error:
        errors.append(f"cannot parse {merged_manifest.relative_to(ROOT)}: {error}")
        continue
    packaged_permissions = {
        element.attrib.get(f"{android_namespace}name", "")
        for element in root.findall("uses-permission")
    }
    unexpected = packaged_permissions - allowed_assembled_permissions
    if unexpected:
        errors.append(
            "unexpected packaged Android permission(s): " + ", ".join(sorted(unexpected))
        )

source_files = [
    *ANDROID_SOURCE.rglob("*.kt"),
]
for path in source_files:
    text = path.read_text(encoding="utf-8")
    if re.search(r"\b(Supabase|Firebase|Appwrite|URLSession|OkHttp|Retrofit)\b", text):
        errors.append(f"service/network API found in I1A source: {path.relative_to(ROOT)}")

for restricted in (ROOT / "supabase/migrations").glob("*.sql"):
    errors.append(f"business migration is outside I1A: {restricted.relative_to(ROOT)}")
for restricted in (ROOT / "supabase/functions").glob("*.ts"):
    errors.append(f"Edge Function is outside I1A: {restricted.relative_to(ROOT)}")

if errors:
    print("Native foundation validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Android foundation validation passed.")
