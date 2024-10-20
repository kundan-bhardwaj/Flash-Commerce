from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(help_text="please enter a number")
    created_at = models.DateField(auto_now=True,editable=False)
    updated_at = models.DateField(auto_now=True)

class Order(models.Model):
    CHOICES = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    )

    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through="OrderItem")
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    ordered_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=10,choices=CHOICES)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, default=None)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)