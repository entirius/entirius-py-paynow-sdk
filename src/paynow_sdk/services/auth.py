# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import base64
import hashlib
import hmac
import json
import uuid
from dataclasses import dataclass


@dataclass
class Authorization:
    api_key: str
    signature_key: str
    signature: str = None
    idempotency_key: str | None = None

    def __post_init__(self):
        if self.idempotency_key is None:
            # Generate random string with maximum length of 45 characters for an Idempotency-Key header.
            # https://docs.paynow.pl/docs/reference/v3/send-payment-request#request
            self.idempotency_key = uuid.uuid4().hex[:45]

    def calculate_signature(self, body=None, parameters=None, is_notification=False):
        if parameters is None:
            parameters = {}

        # Sort headers and parameters by their keys (needed for signature calculation)
        sorted_headers = {"Api-Key": self.api_key, "Idempotency-Key": self.idempotency_key}
        sorted_parameters = {k: parameters[k] for k in sorted(parameters)}

        # Calculating signature for webhook and request is different.
        # Calculating signature for webhook doesn't require headers and parameters, just body
        # Calculating signature for request requires headers and parameters
        # (I digged it from paynow php sdk code :) and it's not in the documentation)
        if is_notification:
            payload = body
        else:
            # order of keys is important 1.headers 2.parameters 3.body
            payload = {
                "headers": sorted_headers,
                "parameters": sorted_parameters if sorted_parameters else {},
                "body": (
                    body if body else ""
                ),  # it's important to have an empty string here, not an empty dict - when body is empty/GET request
            }
        # Convert payload to JSON string, Calculate HMAC SHA256 hash, Encode the hash using Base64
        payload_str = json.dumps(payload, separators=(",", ":"))
        hash_obj = hmac.new(self.signature_key.encode(), payload_str.encode(), hashlib.sha256)
        signature = base64.b64encode(hash_obj.digest()).decode()
        self.signature = signature
        return signature

    def get_auth_header(self):
        headers = {
            "Api-Key": self.api_key,
            "Idempotency-Key": self.idempotency_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.signature:
            headers["Signature"] = self.signature
        return headers
