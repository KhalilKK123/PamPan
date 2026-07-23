# Application contracts

This directory holds versioned schemas, synthetic examples, and approved decision records for the active Android application. Assets remain non-executable. The dormant iOS foundation is not a contract consumer or parity gate unless fresh approval reactivates it.

I2A defines only the local `pantry-contract-v1` preview contract. It is not a Supabase schema, persistence contract, authenticated API, or migration format. All fixtures are synthetic and contain no credentials, tokens, private endpoints, or sensitive user data because this repository is public.

Validate the contract, canonical fixture, Android asset copy, and built-in negative cases with:

```sh
python3 scripts/check-contracts.py
```
