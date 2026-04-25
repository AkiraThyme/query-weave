"""Minimal seed snippet for example project."""

from sample_app.models import Customer, Order, Product


def seed() -> None:
    customer = Customer.objects.create(email="ada@example.com", name="Ada")
    product = Product.objects.create(name="Keyboard", category="Accessories", price=99.99)
    Order.objects.create(customer=customer, product=product, status="completed", quantity=1, price=99.99)
