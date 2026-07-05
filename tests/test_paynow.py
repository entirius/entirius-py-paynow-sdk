# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from paynow_sdk.dto.payment import Address
from paynow_sdk.services.auth import Authorization
from paynow_sdk.services.client import PayNow

API_KEY = "test"
SIGNATURE_KEY = "test"


def test_calculate_signature():
    body = {
        "paymentId": "NOH5-Z20-L0P-HU7",
        "externalId": "0100000106",
        "status": "CONFIRMED",
        "modifiedAt": "2024-08-20T16:46:14",
    }
    signature = Authorization(api_key=API_KEY, signature_key=SIGNATURE_KEY).calculate_signature(
        body=body, parameters={}, is_notification=True
    )
    assert signature


def test_client_init():
    paynow = PayNow(api_key=API_KEY, signature_key=SIGNATURE_KEY, is_sandbox=True)
    assert paynow is not None


def test_dto_address():
    address = Address(street="test", apartmentNumber="", zipcode="01-111", city="test", county="test", country="test")
    assert address.to_dict()["street"] == "test"
