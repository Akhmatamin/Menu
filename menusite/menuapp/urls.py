from django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'user',UserProfileViewSet, basename='users')
router.register(r'cartitem',CartItemViewSet, basename='cartitems')
router.register(r'order',OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('products',ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>',ProductDetailAPIView.as_view(), name='product-detail'),
    path('category',CategoryListAPIView.as_view(), name='category-list'),
    path('category/<int:pk>',CategoryDetailAPIView.as_view(), name='category-detail'),
    path('review',ReviewListAPIView.as_view(), name='review-list'),
    path('review/<int:pk>',ReviewDetailAPIView.as_view(), name='review-detail'),
    path('cart/simple/', CartAPIView.as_view())

]