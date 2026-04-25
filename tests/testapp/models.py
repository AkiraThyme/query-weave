from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    price = models.FloatField()
    rating = models.FloatField(default=0)
    created_at = models.DateField()
