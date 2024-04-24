from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CustomerCreateViewSet, CustomerViewSet

router = DefaultRouter()

router.register(r'customer', CustomerViewSet, basename='customer')

urlpatterns = [
    path('customer/register',
         CustomerCreateViewSet.as_view({'post': 'create'}), name='customer-register'),
] + router.urls
