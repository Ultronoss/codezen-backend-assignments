from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Customer, Seller, Product, Order, PlatformApiCall
from .serializers import CustomerSerializer, SellerSerializer, ProductSerializer, OrderSerializer, PlatformApiCallSerializer

class BaseAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

from django.urls import reverse
from rest_framework.test import APIClient

class CustomerViewSetTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.customer = Customer.objects.create(user=self.user, name='Test Customer')

    def test_list_customers(self):
        url = reverse('customer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_customer(self):
        url = reverse('customer-detail', kwargs={'pk': self.customer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Customer')

    def test_create_customer(self):
        url = reverse('customer-list')
        data = {'name': 'New Customer'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)

    def test_update_customer(self):
        url = reverse('customer-detail', kwargs={'pk': self.customer.id})
        data = {'name': 'Updated Customer'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, 'Updated Customer')

    def test_delete_customer(self):
        url = reverse('customer-detail', kwargs={'pk': self.customer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)

class SellerViewSetTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.seller = Seller.objects.create(user=self.user, name='Test Seller')

    def test_list_sellers(self):
        url = reverse('seller-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_seller(self):
        url = reverse('seller-detail', kwargs={'pk': self.seller.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Seller')

    def test_create_seller(self):
        url = reverse('seller-list')
        data = {'name': 'New Seller'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Seller.objects.count(), 2)

    def test_update_seller(self):
        url = reverse('seller-detail', kwargs={'pk': self.seller.id})
        data = {'name': 'Updated Seller'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.name, 'Updated Seller')

    def test_delete_seller(self):
        url = reverse('seller-detail', kwargs={'pk': self.seller.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Seller.objects.count(), 0)

class ProductViewSetTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.seller = Seller.objects.create(user=self.user, name='Test Seller')
        self.product = Product.objects.create(seller=self.seller, name='Test Product', price=10.00)

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_create_product(self):
        url = reverse('product-list')
        data = {'seller': self.seller.id, 'name': 'New Product', 'price': 15.00}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_update_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.id})
        data = {'name': 'Updated Product', 'price': 20.00}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')
        self.assertEqual(self.product.price, 20.00)

    def test_delete_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

class OrderViewSetTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.customer = Customer.objects.create(user=self.user, name='Test Customer')
        self.seller = Seller.objects.create(user=User.objects.create_user(username='seller', password='pass'), name='Test Seller')
        self.product = Product.objects.create(seller=self.seller, name='Test Product', price=10.00)
        self.order = Order.objects.create(customer=self.customer, seller=self.seller, amount=10.00)
        self.order.products.add(self.product)

    def test_list_orders(self):
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_order(self):
        url = reverse('order-detail', kwargs={'pk': self.order.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], '10.00')

    def test_create_order(self):
        url = reverse('order-list')
        data = {'customer': self.customer.id, 'seller': self.seller.id, 'products': [self.product.id], 'amount': 20.00}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)

    def test_update_order(self):
        url = reverse('order-detail', kwargs={'pk': self.order.id})
        data = {'amount': 15.00}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.amount, 15.00)

    def test_delete_order(self):
        url = reverse('order-detail', kwargs={'pk': self.order.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)

class PlatformApiCallViewSetTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.user.is_staff = True
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.api_call = PlatformApiCall.objects.create(endpoint='/api/test', method='GET', response_time=0.5)

    def test_list_api_calls(self):
        url = reverse('api:platformapicall-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_api_call(self):
        url = reverse('api:platformapicall-detail', kwargs={'pk': self.api_call.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['endpoint'], '/api/test')

class CustomerRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_customer_registration(self):
        url = reverse('customer-registration')
        data = {'username': 'newcustomer', 'password': 'testpass123', 'name': 'New Customer'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(Customer.objects.count(), 1)

class SellerRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_seller_registration(self):
        url = reverse('seller-registration')
        data = {'username': 'newseller', 'password': 'testpass123', 'name': 'New Seller'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(Seller.objects.count(), 1)