# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json

from requests import Response


def validate_paynow_response(response: Response) -> (bool, dict):
    response_body = json.loads(response.text)

    if response.status_code == 200:
        return True, response_body

    if response.status_code == 201:
        return True, response_body

    if response.status_code == 302:
        return True, response_body

    if response.status_code == 400:
        validation, error_message = validate_paynow_response_body_when_error(response_body)
        if validation:
            raise ValueError(error_message)

    if response.status_code == 401:
        validation, error_message = validate_paynow_response_body_when_error(response_body)
        if validation:
            raise ConnectionError(error_message)

    if response.status_code == 403:
        validation, error_message = validate_paynow_response_body_when_error(response_body)
        if validation:
            raise PermissionError(error_message)

    if response.status_code == 404:
        validation, error_message = validate_paynow_response_body_when_error(response_body)
        if validation:
            raise ValueError(error_message)

    if response.status_code == 408:
        validation, error_message = validate_paynow_response_body_when_error(response_body)
        if validation:
            raise TimeoutError(error_message)

    if response.status_code == 500:
        validation, error_message = validate_paynow_response_body_when_error(response_body)
        if validation:
            raise SystemError(error_message)

    if response.status_code == 503:
        validation, error_message = validate_paynow_response_body_when_error(response_body)
        if validation:
            raise BrokenPipeError(error_message)

    return False, response_body


def validate_paynow_response_body_when_error(response_body: dict) -> (bool, str):
    if "statusCode" in response_body and "errors" in response_body:
        error_message = [error_msg["errorType"] + error_msg["message"] for error_msg in response_body["errors"]]
        return True, " | ".join(error_message)
    return False, ""


def validate_paynow_auth_success(response_body: dict) -> bool:
    if (
        "redirectUrl" in response_body
        and "paymentId" in response_body
        and "token_type" in response_body
        and "app_id" in response_body
        and "expires_in" in response_body
        and "nonce" in response_body
    ):
        return True
    return False


def validate_paynow_create_order(response_body: dict) -> bool:
    if "redirectUrl" in response_body and "paymentId" in response_body:
        return True
    return False
