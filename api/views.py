from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer
from .permissions import IsOwner
from .mixins import PlatformApiCallMixin
from .decorators import customer_only
from rest_framework.decorators import action
from rest_framework.response import Response

class OrderViewSet(PlatformApiCallMixin, viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related('customer', 'seller').prefetch_related('products')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Adjust filterset fields
    filterset_fields = ['customer', 'seller', 'amount', 'products']  
    search_fields = ['products__name']  # Searching through product names
    ordering_fields = ['amount', 'created_at']
    ordering = ['created_at']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'customer'):
            # Filter orders by customer linked to the user
            return self.queryset.filter(customer__user=user).select_related('customer', 'seller').prefetch_related('products')
        return self.queryset.none()

    def list(self, request, *args, **kwargs):
        # Apply custom sorting like top 5
        top = request.query_params.get('top', None)
        queryset = self.filter_queryset(self.get_queryset())

        if top:
            queryset = queryset.order_by('-amount')[:5]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ProductViewSet(PlatformApiCallMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['amount', 'name']
    ordering = ['name']