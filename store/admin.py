from django.contrib import admin
from .models import Category, Flower

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'delivery_type', 'in_stock')
    list_filter = ('category', 'delivery_type', 'in_stock')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    fields = (
        'category',
        'title',
        'slug',
        'price',
        'old_price',
        'image',
        'image_url',
        'rating',
        'reviews_count',
        'delivery_type',
        'delivery_price',
        'delivery_time',
        'in_stock',
    )