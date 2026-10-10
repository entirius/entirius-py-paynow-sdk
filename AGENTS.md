# AGENTS.md

Paynow payment gateway SDK — distribution `entirius-py-paynow-sdk`, import `paynow_sdk`.

## Commands

| Command | Meaning |
|---|---|
| `make install` | sync dependencies (uv, incl. extras) |
| `make check` | lint + format-check (ruff) |
| `make fix` | auto-fix lint + format |
| `make test` | test suite (pytest) |

## Conventions

- English only: code, docs, commits, branches, PRs.
- MPL-2.0: every non-trivial source file carries the license header (pre-commit inserts it).
- Toolchain: uv + ruff + hatchling + pytest; all config in `pyproject.toml`; `uv.lock` committed.
- Git flow: `master` (production) + `develop` (integration); changes land via PR; semver tag on `master`.
- Never rename the import package `paynow_sdk` — it is a public API contract.
- Default: do not commit — git is the user's call.
- No AI attribution in commits or PR descriptions.

## Architecture

`src/paynow_sdk/`: `services/client.py` holds the `PayNow` client (create payment, payment status) over the
Paynow REST API; HMAC signing lives in `services/auth.py`, the HTTP wrapper in `services/request.py`, DTOs in
`dto/`, response checks in `validators/`. Runtime dependency: `requests`.
Tests are local (signature, DTO, client init); they make no network call.
