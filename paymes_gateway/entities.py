from dataclasses import dataclass


@dataclass
class Payment:
    status: str
    message: str
    return_url: str
    paymes_order_id: str


@dataclass
class PaymentStatus:
    status: str
    currency: str
    price: str
    type: str
    message: str
    order_id: str
    paymes_order_id: str
    hash: str