# Supabase boundary

This directory is reserved for a future approved local Supabase project, migrations, policy tests, Edge Functions, and synthetic seed data.

I1 and completed I1A deliberately contain:

- no Supabase initialization or linked cloud project;
- no database schema, migration, RLS policy, Storage bucket, Realtime channel, or Edge Function;
- no service URL, publishable key, service-role key, token, or provider secret.

Ordinary future owner-scoped CRUD belongs behind Supabase Auth and RLS. Edge Functions are reserved for privileged, secret-bearing, billable, webhook, push, or coordinated operations.

This repository is public. Any future checked-in configuration must be an explicitly reviewed, redacted template or deliberately publishable client configuration. Never add service-role keys, provider credentials, signing material, live user data, private endpoints, or copied legacy values to source, migrations, fixtures, examples, logs, artifacts, or Git history. See `../SECURITY.md`.
