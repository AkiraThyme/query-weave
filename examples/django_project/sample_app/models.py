from django.db import models


class Customer(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=128)


class Product(models.Model):
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=32)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
