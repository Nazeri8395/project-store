from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from cart.models import Cart, CartItem
from cart.serializers import (AddCartItemSerializer, AddCartSerializer,
                              CartItemSerializer, CartSerializer, 
                              UpdateCartItemSerializer, UpdateCartSerializer)

from drf_yasg.utils import swagger_auto_schema

class CartViewSet(ModelViewSet):

    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return Cart.objects.prefetch_related('items__product').all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartSerializer
        return CartSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        cart = self.get_object()
        if cart.items.count() > 0:
            return Response(
                {'error':'There is some product including this cart.'}, 
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
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
    