from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer, Seller, Product, Order, PlatformApiCall
from .serializers import (
    CustomerSerializer, SellerSerializer, ProductSerializer,
    OrderSerializer, PlatformApiCallSerializer, CustomerRegistrationSerializer,
    SellerRegistrationSerializer
)
from .permissions import IsOwnerOrReadOnly
from .mixins import APILoggingMixin
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomerViewSet(APILoggingMixin, viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class SellerViewSet(APILoggingMixin, viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class ProductViewSet(APILoggingMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class OrderViewSet(APILoggingMixin, viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related('customer', 'seller').prefetch_related('products')
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['products']
    search_fields = ['customer__name', 'seller__name']
    ordering_fields = ['amount', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'customer_profile'):
            return self.queryset.filter(customer__user=user)
        return self.queryset

class PlatformApiCallViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlatformApiCall.objects.all()
    serializer_class = PlatformApiCallSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

class CustomerRegistrationView(generics.CreateAPIView):
    serializer_class = CustomerRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        token, created = Token.objects.get_or_create(user=customer.user)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data['token'] = token.key
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

class SellerRegistrationView(generics.CreateAPIView):
    serializer_class = SellerRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        seller = serializer.save()
        token, created = Token.objects.get_or_create(user=seller.user)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data['token'] = token.key
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)