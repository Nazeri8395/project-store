from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from cart.models import Cart, CartItem
from cart.serializers import AddCartItemSerializer, AddCartSerializer, CartItemSerializer, CartSerializer, UpdateCartItemSerializer, UpdateCartSerializer

from drf_yasg.utils import swagger_auto_schema

class CartViewSet(ModelViewSet):
    # محدود کردن متدهای قابل دسترس (حذف PUT و PATCH)
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        # فقط گرفتن سبد خرید‌ها
        return Cart.objects.prefetch_related('items__product').all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartSerializer
        return CartSerializer

    # @swagger_auto_schema(method='get', responses={200: CartSerializer})
    def list(self, request, *args, **kwargs):
        # نمایش لیست سبد خریدها
        return super().list(request, *args, **kwargs)

    # @swagger_auto_schema(method='post', responses={201: CreateCartSerializer})
    def create(self, request, *args, **kwargs):
        # ایجاد یک سبد خرید جدید
        return super().create(request, *args, **kwargs)

    # @swagger_auto_schema(method='delete', responses={204: 'No Content'})
    def destroy(self, request, *args, **kwargs):
        """ کاملاً حذف کردن یک سبد خرید """
        cart = self.get_object()
        cart.delete()
        return Response({'message': 'Shopping cart deleted.'}, status=status.HTTP_204_NO_CONTENT)
    
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
        
    def get_queryset(self):
        cart_pk = self.kwargs['cart_pk']
        return CartItem.objects.select_related("product").filter(cart_id=cart_pk).all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_pk':self.kwargs['cart_pk']}
    