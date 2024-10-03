from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer, Seller, Product, Order, PlatformApiCall

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'name', 'mobile', 'user']

class SellerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Seller
        fields = ['id', 'name', 'mobile', 'user']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'amount']

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    seller = SellerSerializer(read_only=True)
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'seller', 'products', 'amount', 'created_at']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for product_data in products_data:
            product, created = Product.objects.get_or_create(name=product_data['name'], defaults={'amount': product_data['amount']})
            order.products.add(product)
        return order

class PlatformApiCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformApiCall
        fields = '__all__'

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Customer
        fields = ('id', 'user', 'name', 'mobile')
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        customer = Customer.objects.create(user=user, **validated_data)
        return customer

class SellerRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Seller
        fields = ('id', 'user', 'name', 'mobile')
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        seller = Seller.objects.create(user=user, **validated_data)
        return seller