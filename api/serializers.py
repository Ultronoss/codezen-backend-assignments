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
    customer = CustomerSerializer(read_only=True)
    seller = SellerSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True
    )
    seller_id = serializers.PrimaryKeyRelatedField(
        queryset=Seller.objects.all(), source='seller', write_only=True
    )
    product_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='products', many=True, write_only=True
    )

    class Meta:
        model = Order
        fields = ['id', 'customer', 'seller', 'products', 'customer_id', 'seller_id', 'product_ids', 'amount', 'created_at']

class PlatformApiCallSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PlatformApiCall
        fields = ['id', 'user', 'requested_url', 'requested_data', 'response_data', 'timestamp']
