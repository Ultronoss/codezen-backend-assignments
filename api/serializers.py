from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer, Seller, Product, Order, PlatformApiCall

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'mobile', 'user']

class SellerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Seller
        fields = ['id', 'name', 'mobile', 'user']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'amount']

    def validate_name(self, value):
        if Product.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Product with this name already exists.")
        return value

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all())
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'seller', 'products', 'amount', 'created_at']

class PlatformApiCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformApiCall
        fields = ['id', 'user', 'requested_url', 'requested_data', 'response_data', 'timestamp']