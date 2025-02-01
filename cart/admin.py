from django.contrib import admin

from cart.models import Cart, CartItem

class   CartItemInLine(admin.TabularInline):
    model = CartItem
    fields = ['id', 'product', 'quantity']
    extra = 1
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
    inlines = [CartItemInLine]