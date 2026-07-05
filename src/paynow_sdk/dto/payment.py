# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
from dataclasses import asdict, dataclass


@dataclass
class DTO:
    def to_dict(obj):
        return asdict(obj, dict_factory=lambda x: {k: v for (k, v) in x if v not in [None, [], ""]})


@dataclass
class Phone(DTO):
    prefix: str
    number: int


@dataclass
class Address(DTO):
    street: str | None = None
    houseNumber: str | None = None
    apartmentNumber: str | None = None
    zipcode: str | None = None
    city: str | None = None
    county: str | None = None
    country: str | None = None

    def __post_init__(self):
        requirements = {
            "street": (self.street, 100, 1),
            "houseNumber": (self.houseNumber, 16, 0),
            "apartmentNumber": (self.apartmentNumber, 16, 0),
            "zipcode": (self.zipcode, 10, 1, r"^[A-Z0-9-_ ]+$"),
            "city": (self.city, 100, 2),
            "county": (self.county, 50, 0),
            "country": (self.country, 2, 2),
        }
        for key, (value, max_len, min_len, *regex) in requirements.items():
            if value:
                if len(value) > max_len:
                    setattr(self, key, value[:max_len])
                if len(value) < min_len:
                    delattr(self, key)
                if regex and not re.match(regex[0], value):
                    setattr(self, key, re.sub(r"[^A-Z0-9-_ ]", "", value))


@dataclass
class AllAddresses(DTO):
    billing: Address | None = None
    shipping: Address | None = None


@dataclass
class Buyer(DTO):
    email: str
    firstName: str | None = None
    lastName: str | None = None
    phone: Phone | None = None
    address: AllAddresses | None = None


@dataclass
class OrderItem(DTO):
    name: str
    quantity: int
    price: int
    category: str


@dataclass
class Payment(DTO):
    amount: int
    currency: str
    description: str
    externalId: str
    buyer: Buyer
    orderItems: list[OrderItem]
    continueUrl: str | None = None
    validityTime: int | None = None
