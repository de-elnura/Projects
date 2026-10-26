from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default="fa-spa")

    def __str__(self):
        return self.name

class Flower(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='flowers')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    price = models.PositiveIntegerField(default=0)
    old_price = models.PositiveIntegerField(default=0, null=True, blank=True)
    image_url = models.CharField(max_length=500, blank=True, default='')
    delivery_type = models.CharField(max_length=50, default="free")
    delivery_price = models.PositiveIntegerField(default=0)
    delivery_time = models.CharField(max_length=100, default="Bugun 2 soatda")
    rating = models.FloatField(default=5.0)
    reviews_count = models.PositiveIntegerField(default=15)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def monthly_installment(self):
        return int(self.price / 12)

# Buyurtmalar va savdo tarixi modeli
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda ⏳'),
        ('delivering', 'Kuryer yo\'lda 🚚'),
        ('delivered', 'Yetkazib berildi ✅'),
        ('cancelled', 'Bekor qilindi ❌'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=150, verbose_name="Qabul qiluvchi ismi")
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami")
    address = models.TextField(verbose_name="Yetkazib berish manzili")
    delivery_method = models.CharField(max_length=50, default="express")
    delivery_time = models.CharField(max_length=100, default="1-2 soat ichida")
    greeting_card = models.TextField(blank=True, null=True, verbose_name="Tabrik xati")
    is_anonymous = models.BooleanField(default=False, verbose_name="Anonim yuborish")
    total_price = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='delivering')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    flower = models.ForeignKey(Flower, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.flower.title} x {self.quantity}"