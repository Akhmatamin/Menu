from .models import *
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone_number']


class ProductListSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(source="get_avg_rating", read_only=True)
    reviews_count = serializers.IntegerField(source="get_count_user", read_only=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'product_name',
            'product_image',
            'product_price',
            'avg_rating',
            'reviews_count',
        ]

class ProductDetailSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(source="get_avg_rating", read_only=True)
    reviews_count = serializers.IntegerField(source="get_count_user", read_only=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'product_name',
            'product_description',
            'product_image',
            'product_price',
            'avg_rating',
            'reviews_count',
            'product_category',
            'size'
        ]


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(source='product_category', many=True,read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_description', 'products']

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user','rating','comment']

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

