# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import logging

from paynow_sdk.dto.payment import Payment
from paynow_sdk.exceptions import PayNowError
from paynow_sdk.services.auth import Authorization
from paynow_sdk.services.request import Request
from paynow_sdk.validators.response import validate_paynow_create_order, validate_paynow_response

logger_process = logging.getLogger("process")


class PayNow:
    is_sandbox: bool
    authorization: Authorization = None

    def __init__(self, api_key: str, signature_key: str, is_sandbox: bool = True):
        self.is_sandbox = is_sandbox

        if not api_key:
            raise PayNowError("API key is required.")

        if not signature_key:
            raise PayNowError("Signature key is required.")

        self.authorization = Authorization(api_key=api_key, signature_key=signature_key)

    def create_payment(self, payment_data: Payment):
        """Creates order in paynow. This request return response with 4 links:"""

        request = Request(
            method="POST",
            resource="payments",
            headers=self.authorization.get_auth_header(),
            data=json.dumps(payment_data.to_dict()),
        )
        self.authorization.calculate_signature(body=request.data, parameters=request.params)
        request.headers = self.authorization.get_auth_header()
        response = request.make_request(self.is_sandbox)
        validation, response_body = validate_paynow_response(response)
        if validation:
            success = validate_paynow_create_order(response_body)
            if success:
                return response_body.get("paymentId"), response_body.get("redirectUrl"), self.authorization.signature
            else:
                logger_process.error(
                    "PayNow API response failed",
                    extra={"details": {"request_params": request.params, "response_body": response_body}},
                )
                raise PayNowError("PayNow response is not correct.")
        else:
            logger_process.error(
                "PayNow API response failed",
                extra={"details": {"request_params": request.params, "response_body": response_body}},
            )
            raise PayNowError(f"The PayNow API responded with an error. Message: {response_body.get('message')}")

    def get_payment_status(self, payment_id: str):
        """Get payment status from paynow. This request return response with payment status"""

        request = Request(
            method="GET", resource=f"payments/{payment_id}/status", headers=self.authorization.get_auth_header()
        )
        self.authorization.calculate_signature(parameters=request.params)
        request.headers = self.authorization.get_auth_header()
        response = request.make_request(self.is_sandbox)
        validation, response_body = validate_paynow_response(response)
        if validation:
            return response_body.get("status")
        else:
            logger_process.error(
                "PayNow API response failed",
                extra={"details": {"request_params": request.params, "response_body": response_body}},
            )
            raise PayNowError(f"The PayNow API responded with an error. Message: {response_body.get('message')}")
