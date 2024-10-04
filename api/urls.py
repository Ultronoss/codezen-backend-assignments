from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, ProductViewSet

from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]