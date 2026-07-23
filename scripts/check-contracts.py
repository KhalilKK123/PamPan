#!/usr/bin/env python3
"""Validate the approved I2A pantry contract with Python's standard library."""

from __future__ import annotations

from copy import deepcopy
from datetime import date
from decimal import Decimal
import json
from pathlib import Path
import re
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "contracts/schemas/pantry-contract-v1.schema.json"
EXAMPLE_PATH = ROOT / "contracts/examples/pantry-contract-v1.sample.json"
ANDROID_ASSET_PATH = (
    ROOT
    / "apps/android/app/src/main/assets/pantry-contract-v1.sample.json"
)

ROOT_KEYS = {"contractVersion", "categories", "items"}
CATEGORY_KEYS = {"id", "name"}
ITEM_KEYS = {"id", "name", "quantity", "unit", "expiryDate", "categoryId"}
QUANTITY_PATTERN = re.compile(
    r"^\+?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?$"
)
CONTRACT_WHITESPACE = (
    r"\u0009-\u000D\u0020\u0085\u00A0\u1680\u2000-\u200A"
    r"\u2028-\u2029\u202F\u205F\u3000\uFEFF"
)
NONBLANK_PATTERN = re.compile(
    rf"^[\s\S]*[^{CONTRACT_WHITESPACE}][\s\S]*$"
)
UNIT_PATTERN = re.compile(
    rf"^(?:[^{CONTRACT_WHITESPACE}]|"
    rf"[^{CONTRACT_WHITESPACE}][\s\S]*[^{CONTRACT_WHITESPACE}])$"
)
DATE_PATTERN = re.compile(
    r"^(?!0000)[0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])$"
)


class DuplicateKeyError(ValueError):
    """Raised when JSON contains a duplicate object key."""


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
        parse_float=Decimal,
        parse_int=Decimal,
    )


def require_exact_keys(
    value: Any,
    expected: set[str],
    location: str,
    errors: list[str],
) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{location} must be an object")
        return False
    actual = set(value)
    if actual != expected:
        errors.append(
            f"{location} keys must be exactly {sorted(expected)}; got {sorted(actual)}"
        )
        return False
    return True


def validate_nonblank(value: Any, location: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not NONBLANK_PATTERN.fullmatch(value):
        errors.append(f"{location} must be a nonblank string")


def validate_document(document: Any) -> list[str]:
    errors: list[str] = []
    if not require_exact_keys(document, ROOT_KEYS, "root", errors):
        return errors

    if document["contractVersion"] != "1":
        errors.append("contractVersion must be the string '1'")

    categories = document["categories"]
    items = document["items"]
    if not isinstance(categories, list) or not categories:
        errors.append("categories must be a nonempty array")
        categories = []
    if not isinstance(items, list):
        errors.append("items must be an array")
        items = []

    category_ids: set[str] = set()
    for index, category in enumerate(categories):
        location = f"categories[{index}]"
        if not require_exact_keys(category, CATEGORY_KEYS, location, errors):
            continue
        validate_nonblank(category["id"], f"{location}.id", errors)
        validate_nonblank(category["name"], f"{location}.name", errors)
        if isinstance(category["id"], str):
            if category["id"] in category_ids:
                errors.append(f"{location}.id must be unique")
            category_ids.add(category["id"])

    item_ids: set[str] = set()
    for index, item in enumerate(items):
        location = f"items[{index}]"
        if not require_exact_keys(item, ITEM_KEYS, location, errors):
            continue
        for field in ("id", "name", "categoryId"):
            validate_nonblank(item[field], f"{location}.{field}", errors)

        if isinstance(item["id"], str):
            if item["id"] in item_ids:
                errors.append(f"{location}.id must be unique")
            item_ids.add(item["id"])

        quantity = item["quantity"]
        if not isinstance(quantity, str) or not QUANTITY_PATTERN.fullmatch(quantity):
            errors.append(
                f"{location}.quantity must be a nonnegative decimal string"
            )

        unit = item["unit"]
        if (
            not isinstance(unit, str)
            or not UNIT_PATTERN.fullmatch(unit)
        ):
            errors.append(f"{location}.unit must be a trimmed nonblank string")

        expiry = item["expiryDate"]
        if not isinstance(expiry, str) or not DATE_PATTERN.fullmatch(expiry):
            errors.append(f"{location}.expiryDate must use exact YYYY-MM-DD form")
        else:
            try:
                if date.fromisoformat(expiry).isoformat() != expiry:
                    errors.append(f"{location}.expiryDate must be canonical")
            except ValueError:
                errors.append(f"{location}.expiryDate must be a real calendar date")

        category_id = item["categoryId"]
        if isinstance(category_id, str) and category_id not in category_ids:
            errors.append(f"{location}.categoryId must resolve to a category")

    return errors


def validate_schema_shape(schema: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(schema, dict):
        return ["schema must be an object"]
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("schema must declare JSON Schema draft 2020-12")
    if schema.get("$id") != "urn:pampan:pantry-contract:v1":
        errors.append("schema must retain the approved v1 identifier")
    if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        errors.append("schema root must be a closed object")
    if set(schema.get("required", [])) != ROOT_KEYS:
        errors.append("schema root required fields do not match the v1 contract")
    if set(schema.get("properties", {})) != ROOT_KEYS:
        errors.append("schema root properties do not match the v1 contract")
    properties = schema.get("properties", {})
    if properties.get("contractVersion") != {"const": "1"}:
        errors.append("schema contractVersion must be the string constant '1'")
    if properties.get("categories") != {
        "type": "array",
        "minItems": 1,
        "items": {"$ref": "#/$defs/category"},
    }:
        errors.append("schema categories definition does not match the v1 contract")
    if properties.get("items") != {
        "type": "array",
        "items": {"$ref": "#/$defs/item"},
    }:
        errors.append("schema items definition does not match the v1 contract")

    definitions = schema.get("$defs")
    if not isinstance(definitions, dict):
        return [*errors, "schema must define $defs"]
    if set(definitions) != {
        "nonblank",
        "quantity",
        "unit",
        "expiryDate",
        "category",
        "item",
    }:
        errors.append("schema definitions do not match the v1 contract")
        return errors

    for name, expected_keys in (
        ("category", CATEGORY_KEYS),
        ("item", ITEM_KEYS),
    ):
        definition = definitions.get(name, {})
        if (
            definition.get("type") != "object"
            or definition.get("additionalProperties") is not False
            or set(definition.get("required", [])) != expected_keys
            or set(definition.get("properties", {})) != expected_keys
        ):
            errors.append(f"schema {name} definition must be a closed exact object")

    if definitions.get("quantity", {}).get("pattern") != QUANTITY_PATTERN.pattern:
        errors.append("schema quantity pattern does not match validator semantics")
    if definitions.get("expiryDate", {}).get("pattern") != DATE_PATTERN.pattern:
        errors.append("schema expiry-date pattern does not match validator semantics")
    if definitions.get("expiryDate", {}).get("format") != "date":
        errors.append("schema expiry date must declare the date format")
    if definitions.get("nonblank") != {
        "type": "string",
        "minLength": 1,
        "pattern": NONBLANK_PATTERN.pattern,
    }:
        errors.append("schema nonblank definition does not match validator semantics")
    if definitions.get("quantity", {}).get("type") != "string":
        errors.append("schema quantity must be encoded as a string")
    if definitions.get("unit") != {
        "type": "string",
        "minLength": 1,
        "pattern": UNIT_PATTERN.pattern,
    }:
        errors.append("schema unit definition does not match validator semantics")
    if definitions.get("expiryDate", {}).get("type") != "string":
        errors.append("schema expiry date must be encoded as a string")

    expected_category_properties = {
        "id": {"$ref": "#/$defs/nonblank"},
        "name": {"$ref": "#/$defs/nonblank"},
    }
    if definitions.get("category", {}).get("properties") != expected_category_properties:
        errors.append("schema category fields do not use the approved definitions")

    expected_item_properties = {
        "id": {"$ref": "#/$defs/nonblank"},
        "name": {"$ref": "#/$defs/nonblank"},
        "quantity": {"$ref": "#/$defs/quantity"},
        "unit": {"$ref": "#/$defs/unit"},
        "expiryDate": {"$ref": "#/$defs/expiryDate"},
        "categoryId": {"$ref": "#/$defs/nonblank"},
    }
    if definitions.get("item", {}).get("properties") != expected_item_properties:
        errors.append("schema item fields do not use the approved definitions")
    return errors


def expect_invalid(
    canonical: dict[str, Any],
    label: str,
    mutate: Any,
    failures: list[str],
) -> None:
    candidate = deepcopy(canonical)
    mutate(candidate)
    if not validate_document(candidate):
        failures.append(f"negative case unexpectedly passed: {label}")


def run_negative_cases(canonical: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    cases = [
        ("blank category id", lambda value: value["categories"][0].update(id=" ")),
        ("blank category name", lambda value: value["categories"][0].update(name="")),
        ("blank item id", lambda value: value["items"][0].update(id="\t")),
        ("blank item name", lambda value: value["items"][0].update(name=" ")),
        (
            "unicode blank category id",
            lambda value: value["categories"][0].update(id="\u0085"),
        ),
        (
            "unicode blank item name",
            lambda value: value["items"][0].update(name="\ufeff"),
        ),
        ("malformed date", lambda value: value["items"][0].update(expiryDate="2026-8-15")),
        ("invalid date", lambda value: value["items"][0].update(expiryDate="2026-02-30")),
        ("negative quantity", lambda value: value["items"][0].update(quantity="-1")),
        ("nondecimal quantity", lambda value: value["items"][0].update(quantity="one")),
        ("numeric quantity", lambda value: value["items"][0].update(quantity=1)),
        ("blank unit", lambda value: value["items"][0].update(unit=" ")),
        ("untrimmed unit", lambda value: value["items"][0].update(unit=" kg")),
        (
            "unicode untrimmed unit prefix",
            lambda value: value["items"][0].update(unit="\ufeffkg"),
        ),
        (
            "unicode untrimmed unit suffix",
            lambda value: value["items"][0].update(unit="kg\u0085"),
        ),
        (
            "unresolved category",
            lambda value: value["items"][0].update(categoryId="category-missing"),
        ),
        (
            "duplicate category id",
            lambda value: value["categories"][1].update(
                id=value["categories"][0]["id"]
            ),
        ),
        (
            "duplicate item id",
            lambda value: value["items"][1].update(id=value["items"][0]["id"]),
        ),
        ("unexpected root field", lambda value: value.update(owner="sample")),
        (
            "unexpected category field",
            lambda value: value["categories"][0].update(order=1),
        ),
        (
            "unexpected item field",
            lambda value: value["items"][0].update(timestamp="2026-01-01"),
        ),
        ("wrong version", lambda value: value.update(contractVersion="2")),
    ]
    for label, mutate in cases:
        expect_invalid(canonical, label, mutate, failures)
    return failures


def run_decimal_acceptance_cases(canonical: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    accepted_spellings = ("01", ".5", "1.", "1e3", "+1.25", "1e9999999999")
    for spelling in accepted_spellings:
        candidate = deepcopy(canonical)
        candidate["items"][0]["quantity"] = spelling
        errors = validate_document(candidate)
        if errors:
            failures.append(
                f"approved decimal spelling unexpectedly failed: {spelling}"
            )
    return failures


def main() -> int:
    failures: list[str] = []
    for path in (SCHEMA_PATH, EXAMPLE_PATH, ANDROID_ASSET_PATH):
        if not path.is_file():
            failures.append(f"missing required contract path: {path.relative_to(ROOT)}")

    if failures:
        print("Contract validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    try:
        schema = load_json(SCHEMA_PATH)
        canonical = load_json(EXAMPLE_PATH)
        android_asset = load_json(ANDROID_ASSET_PATH)
    except (json.JSONDecodeError, DuplicateKeyError, OSError) as error:
        print(f"Contract validation failed:\n- invalid JSON: {error}")
        return 1

    failures.extend(validate_schema_shape(schema))
    failures.extend(validate_document(canonical))
    failures.extend(run_negative_cases(canonical))
    failures.extend(run_decimal_acceptance_cases(canonical))

    if len(canonical.get("items", [])) != 3:
        failures.append("canonical I2A fixture must contain exactly three items")
    if android_asset != canonical:
        failures.append("Android pantry fixture must match the canonical fixture")
    if ANDROID_ASSET_PATH.read_bytes() != EXAMPLE_PATH.read_bytes():
        failures.append("Android pantry fixture must be byte-identical to the canonical fixture")

    if failures:
        print("Contract validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "Pantry contract v1 validation passed "
        "(canonical fixture, 22 negative cases, and 6 decimal spellings)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
