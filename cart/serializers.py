from rest_framework import serializers

from products.models import Product
from .models import Cart, CartItem

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price']
        read_only = ['product_name', 'price']
        
    
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
    
class AddCartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

    def create(self,validated_data):
        cart_id = self.context['cart_pk']
        
        product = validated_data.get("product")
        quantity = validated_data.get("quantity")
        
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product.id)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)
        
        self.instance = cart_item
        return cart_item

class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    item_total = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'item_total']
        
    def get_item_total(self, cart_item):
        return cart_item.quantity * cart_item.product.price
        
class UpdateCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['created_at', 'items']

    
class AddCartSerializer(serializers.ModelSerializer):
    items = AddCartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items']
        read_only = ['id',]
    
    def create(self, validated_data):
        """ ایجاد یک سبد خرید همراه با آیتم‌های آن """
        items_data = validated_data.pop('items', [])  # دریافت آیتم‌های ارسال شده
        cart = Cart.objects.create(**validated_data)  # ایجاد سبد خرید

        for item in items_data:
            CartItem.objects.create(cart=cart, **item)  # ایجاد هر آیتم مرتبط با سبد خرید

        return cart

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        read_only_fields = ['id',]
        
    def get_total_price(self,cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])