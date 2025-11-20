from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    category_name = models.CharField(max_length=24,unique=True)
    category_description = models.TextField()

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name = models.CharField(max_length=24,unique=True)
    product_description = models.TextField()
    product_image = models.ImageField(upload_to="productImages/")
    product_price = models.FloatField()
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_category")
    SIZE_CHOICES = (
        ('Small', 'Small'),
        ('Half', 'Half'),
        ('Full', 'Full'),
    )
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, default='Full')

    def get_avg_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum([i.rating for i in reviews ]) / len(reviews),1)
        return 0

    def get_count_user(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return reviews.count()
        return 0

    def __str__(self):
        return self.product_name

class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1,6)])
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} reviewed {self.product.product_name}"

class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name

    def get_final_price(self):
        return sum([i.get_total_price() for i in self.items.all()])

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.product},{self.quantity}"

    def get_total_price(self):
        return self.quantity * self.product.product_price

class Order(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='orders')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    ORDER_STATUS = (
        ('processing','processing'),
        ('delivered','delivered'),
        ('cancelled','cancelled')
    )
    order_status = models.CharField(max_length=64,choices=ORDER_STATUS,default='processing')
    delivery_address = models.CharField(max_length=120)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.order_status}'


