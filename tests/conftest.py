from datetime import date

import pytest

from tests.testapp.models import Customer, Order, Product


@pytest.fixture
def order_data(db):
    customer = Customer.objects.create(name="Alice")
    book = Product.objects.create(name="Book", category="Books")
    toy = Product.objects.create(name="Toy", category="Toys")
    Order.objects.create(customer=customer, product=book, status="completed", price=100, rating=4.0, created_at=date(2026, 1, 10))
    Order.objects.create(customer=customer, product=toy, status="completed", price=75, rating=5.0, created_at=date(2026, 1, 11))
    Order.objects.create(customer=customer, product=book, status="pending", price=30, rating=2.0, created_at=date(2026, 2, 1))
    return Order.objects.all()
