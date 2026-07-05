# paynow-sdk

Paynow payment gateway SDK — payments, status checks, and notification signature verification
over the Paynow REST API.

## Installation

```shell
pip install entirius-py-paynow-sdk
```

## Usage

```python
from paynow_sdk.services.client import PayNow

paynow = PayNow(api_key="...", signature_key="...", is_sandbox=True)
```

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest)
```

Development and agent instructions: [AGENTS.md](AGENTS.md).

## License

Mozilla Public License 2.0 — see [LICENSE](LICENSE).
