from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, Product, PlatformApiCall
from .serializers import OrderSerializer, ProductSerializer, PlatformApiCallSerializer
from .permissions import IsOwnerOrAdmin
from .mixins import PlatformApiCallMixin
from rest_framework.response import Response

class OrderViewSet(PlatformApiCallMixin, viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related('customer', 'seller').prefetch_related('products')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['customer', 'seller', 'amount', 'products']
    search_fields = ['products__name']
    ordering_fields = ['amount', 'created_at']
    ordering = ['created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset.all().select_related('customer', 'seller').prefetch_related('products')
        elif hasattr(user, 'customer'):
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

class PlatformApiCallViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlatformApiCall.objects.all()
    serializer_class = PlatformApiCallSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Only admins can view API calls

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
