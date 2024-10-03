from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id} by {self.customer.name}'

class PlatformApiCall(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    requested_url = models.URLField()
    requested_data = models.TextField()
    response_data = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'API Call by {self.user} at {self.timestamp}'