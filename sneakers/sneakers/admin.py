from django.contrib import admin
from .models import SneakerColor, SneakerBrand, Sneaker, Cart, CartItem, SneakerLike, Order, OrderItem

@admin.register(SneakerColor)
class SneakerColorAdmin(admin.ModelAdmin):
    list_display = ('color_code', 'color_name')
    search_fields = ('color_name',)

@admin.register(SneakerBrand)
class SneakerBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

@admin.register(Sneaker)
class SneakerAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'price', 'size', 'color', 'stock', 'created_at', 'updated_at')
    search_fields = ('brand__name', 'model', 'color__color_name')
    list_filter = ('brand', 'color', 'size')
    ordering = ('-created_at',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'sneaker', 'quantity')
    search_fields = ('cart__user__username', 'sneaker__model')
    list_filter = ('cart',)

@admin.register(SneakerLike)
class SneakerLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'sneaker', 'liked_at')
    search_fields = ('user__username', 'sneaker__model')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'address', 'created_at', 'status')
    search_fields = ('user__username', 'email', 'address')
    list_filter = ('status', 'created_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'sneaker', 'quantity', 'price')
    search_fields = ('order__id', 'sneaker__model')
