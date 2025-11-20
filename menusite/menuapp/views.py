from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class ReviewListAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer

class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CartAPIView(APIView):
    def get(self, request):
        if request.user.is_anonymous:
            return Response({"error": "login required"}, status=401)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = CartItem.objects.filter(cart=cart)

        return Response({
            "items": CartItemSerializer(items, many=True).data,
            "total": cart.get_final_price()
        })

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=request.data["product_id"])
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if "quantity" in request.data:
            item.quantity = int(request.data["quantity"])
        else:
            item.quantity += 1

        item.save()

        return Response({"message": "ok", "qty": item.quantity})

