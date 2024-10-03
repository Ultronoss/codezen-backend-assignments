from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, SellerViewSet, ProductViewSet,
    OrderViewSet, PlatformApiCallViewSet, CustomerRegistrationView, SellerRegistrationView
)
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'sellers', SellerViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'api-calls', PlatformApiCallViewSet, basename='api-calls')


urlpatterns = [
    path('auth/', obtain_auth_token),
    path('register/customer/', CustomerRegistrationView.as_view(), name='customer-registration'),
    path('register/seller/', SellerRegistrationView.as_view(), name='seller-registration'),
    path('', include(router.urls)),
]