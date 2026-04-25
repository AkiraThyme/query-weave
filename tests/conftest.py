import os
from datetime import date

import django
import pytest
from django.core.management import call_command
from django.test.utils import (
    setup_databases,
    setup_test_environment,
    teardown_databases,
    teardown_test_environment,
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
django.setup()


@pytest.fixture(scope="session", autouse=True)
def _django_test_environment():
    setup_test_environment()
    db_cfg = setup_databases(verbosity=0, interactive=False)
    try:
        yield
    finally:
        teardown_databases(db_cfg, verbosity=0)
        teardown_test_environment()


@pytest.fixture
def db(_django_test_environment):
    call_command("flush", verbosity=0, interactive=False)
    yield


@pytest.fixture
def order_data(db):
    from tests.testapp.models import Customer, Order, Product

    customer = Customer.objects.create(name="Alice")
    book = Product.objects.create(name="Book", category="Books")
    toy = Product.objects.create(name="Toy", category="Toys")
    Order.objects.create(
        customer=customer,
        product=book,
        status="completed",
        price=100,
        rating=4.0,
        created_at=date(2026, 1, 10),
    )
    Order.objects.create(
        customer=customer,
        product=toy,
        status="completed",
        price=75,
        rating=5.0,
        created_at=date(2026, 1, 11),
    )
    Order.objects.create(
        customer=customer,
        product=book,
        status="pending",
        price=30,
        rating=2.0,
        created_at=date(2026, 2, 1),
    )
    return Order.objects.all()
