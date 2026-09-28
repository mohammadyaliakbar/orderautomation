from datetime import date
from decimal import Decimal

from app.exporter import format_order, format_order_dict, format_orders_summary
from app.processor import Order, OrderStatus

SAMPLE_ORDER = Order(
    id=1054,
    customer="Grace Okafor",
    customer_email="grace.okafor@example.com",
    shipping_address="106 Market Street, Springfield, 10006",
    product="Portable SSD 1TB Classic",
    product_id=10,
    quantity=2,
    total=Decimal("611.64"),
    status=OrderStatus.PROCESSING,
    date=date(2025, 9, 7),
)


def test_format_order_contains_key_info():
    result = format_order(SAMPLE_ORDER)

    assert "1054" in result
    assert "Grace Okafor" in result
    assert "Portable SSD 1TB Classic" in result
    assert "611.64" in result


def test_format_orders_summary_empty_list():
    result = format_orders_summary([])
    assert "هیچ سفارشی" in result


def test_format_orders_summary_with_orders():
    result = format_orders_summary([SAMPLE_ORDER])
    assert "1 سفارش" in result
    assert "1054" in result


def test_export_to_dict_returns_correct_structure():
    result = format_order_dict(SAMPLE_ORDER)

    assert result["id"] == 1054
    assert result["total"] == "611.64"
    assert result["status"] == "processing"
    assert result["date"] == "2025-09-07"
