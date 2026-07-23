# Pantry contract v1 decision

Status: approved for `PAMPAN-NATIVE-REWRITE / I2A` only.

This decision defines the minimal local contract used by the offline Android pantry
preview. It is not a cloud schema, persistence format, authenticated API, or
migration contract.

## Required semantics

- Item and category IDs are required opaque, nonblank strings.
- Item and category names are required nonblank strings.
- Each item refers to its category by category ID.
- Expiry dates are required real calendar dates encoded exactly as ISO
  `YYYY-MM-DD`.
- Quantities are required nonnegative arbitrary-precision decimals. JSON fixtures
  encode them as strings to avoid binary floating-point loss.
- Units are required trimmed, nonblank, case-preserving free-form strings.

The canonical fixture preserves declaration order only to make the preview
deterministic. This does not define general pantry ordering.

## Deliberately undefined

The contract defines no owner, timestamps, normalization, uniqueness of names,
length limits, sorting, searching, maximum quantity, fixed scale, rounding,
arithmetic, unit catalog, conversion, relative-expiry calculation, mutation, or
deletion semantics.

The fixture contains only synthetic sample data. It must never contain production,
personal, legacy-user, credential, endpoint, or signing data.
