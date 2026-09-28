from datetime import date
from decimal import Decimal

import pytest

from app.processor import InvalidOrderError, OrderStatus, clean_order, clean_orders

VALID_ORDER = {
    "id": 1054,
    "customer": "aliakbar",
    "customer_email": "ali@gmail.com",
    "shipping_address": "abdol abad city keyaban 1080",
    "product": "Iphon19",
    "product_id": 109,
    "quantity": 2,
    "total": 10000.42,
    "status": "processing",
    "date": "2025-08-13",
}


def test_clean_order():
    order = clean_order(VALID_ORDER)
    assert order.id == 1054
    assert order.customer == "aliakbar"
    assert order.customer_email == "ali@gmail.com"
    assert order.shipping_address == "abdol abad city keyaban 1080"
    assert order.product == "Iphon19"
    assert order.product_id == 109
    assert order.quantity == 2
    assert order.total == Decimal("10000.42")
    assert order.status == OrderStatus.PROCESSING
    assert order.date == date(2025, 8, 13)


def test_clean_order_missing_field():
    broken = VALID_ORDER.copy()
    del broken["customer"]

    with pytest.raises(InvalidOrderError):
        clean_order(broken)


def test_clean_order_numeric_field():
    broken = VALID_ORDER.copy()
    broken["product_id"] = "one"

    with pytest.raises(InvalidOrderError):
        clean_order(broken)


def test_clean_order_invalid_email():
    broken = VALID_ORDER.copy()
    broken["customer_email"] = "not_an_email"

    with pytest.raises(InvalidOrderError):
        clean_order(broken)


def test_clean_order_negative_total():
    broken = VALID_ORDER.copy()
    broken["total"] = -100

    with pytest.raises(InvalidOrderError):
        clean_order(broken)


def test_clean_order_zero_quantity():
    broken = VALID_ORDER.copy()
    broken["quantity"] = 0

    with pytest.raises(InvalidOrderError):
        clean_order(broken)


def test_clean_orders_skip_order():
    broken = VALID_ORDER.copy()
    broken["customer"] = "mohammad"
    broken["status"] = "invalid_status"

    orders = {"orders": [VALID_ORDER, broken]}
    result = clean_orders(orders)

    assert len(result) == 1
    assert result[0].id == 1054


def test_clean_orders_empty():
    result = clean_orders({"orders": []})

    assert result == []


def test_clean_orders_missing_orders():
    result = clean_orders({})

    assert result == []
