# entirius-py-paynow-sdk

A Python client for the Paynow payment gateway REST API, part of Entirius, the open-source modular ecommerce platform.
It creates payments, reads their status and signs requests and notifications behind one `PayNow` class.

[![PyPI](https://img.shields.io/pypi/v/entirius-py-paynow-sdk.svg)](https://pypi.org/project/entirius-py-paynow-sdk/)
[![Python](https://img.shields.io/pypi/pyversions/entirius-py-paynow-sdk.svg)](https://pypi.org/project/entirius-py-paynow-sdk/)
[![License: MPL-2.0](https://img.shields.io/badge/license-MPL--2.0-blue.svg)](https://github.com/entirius/entirius-py-paynow-sdk/blob/develop/LICENSE)

## What it does

- Creates a payment from a typed `Payment` DTO (`create_payment()`).
- Reads the status of a payment by its id (`get_payment_status()`).
- Calculates the HMAC SHA-256 signature of a request or of a notification body (`Authorization.calculate_signature()`).
- Targets the sandbox or the production API with the `is_sandbox` flag.

## Installation

```shell
uv add entirius-py-paynow-sdk
pip install entirius-py-paynow-sdk
```

The import name is `paynow_sdk`.

## Quick start

```python
from paynow_sdk.services.client import PayNow

paynow = PayNow(api_key="...", signature_key="...", is_sandbox=True)
status = paynow.get_payment_status("<payment-id>")
```

## Requirements

- Python 3.11 or newer.
- `requests` (installed as a dependency).
- A Paynow merchant account (API key and signature key); a sandbox account for testing.

## Documentation

- Entirius documentation: https://docs.entirius.com/
- Changelog: https://github.com/entirius/entirius-py-paynow-sdk/blob/develop/CHANGELOG.md

## Part of Entirius

This SDK is one of the payment gateway clients used by the Entirius backend service (Volkanos) and its modules.

- Backend service: https://github.com/entirius/entirius-service-volkanos
- Docker harness: https://github.com/entirius/entirius-zeno
- Checkout module: https://github.com/entirius/entirius-django-checkout
- Sibling gateway SDKs: https://github.com/entirius/entirius-py-payu-sdk, https://github.com/entirius/entirius-py-autopay-sdk, https://github.com/entirius/entirius-py-paypal-sdk

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest)
```

Development and agent instructions: https://github.com/entirius/entirius-py-paynow-sdk/blob/develop/AGENTS.md

## License

Mozilla Public License 2.0 (MPL-2.0) — see https://github.com/entirius/entirius-py-paynow-sdk/blob/develop/LICENSE.
