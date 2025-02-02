from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from cart.models import Cart, CartItem
from cart.serializers import (AddCartItemSerializer, AddCartSerializer,
                              CartItemSerializer, CartSerializer, 
                              UpdateCartItemSerializer, UpdateCartSerializer)

@extend_schema_view(
    list=extend_schema(
        summary="Get shopping cart list",
        description="This API returns a list of existing shopping carts..",
        responses={200: CartSerializer}
    ),
    create=extend_schema(
        summary="Create a new shopping cart",
        description="Creates a new shopping cart and returns its ID..",
        request=AddCartSerializer,
        responses={201: CartSerializer}
    ),
    destroy=extend_schema(
        summary="Delete a shopping cart",
        description="Deletes a shopping cart if it contains no items..",
        responses={
            204: {"description": "Shopping cart deleted."},
            405: {"description": "There is some product including this cart."}
        }
    ),
)
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
    
@extend_schema_view(
    list=extend_schema(
        summary="Get items from a shopping cart",
        description="Returns the list of items in a specific shopping cart..",
        responses={200: CartItemSerializer}
    ),
    create=extend_schema(
        summary="Add a product to cart",
        description="Adds a new product to the cart..",
        request=AddCartItemSerializer,
        responses={201: CartItemSerializer}
    ),
    partial_update=extend_schema(
        summary="Edit the quantity of an item in the shopping cart",
        description="Changes the quantity of a specific product in the shopping cart..",
        request=UpdateCartItemSerializer,
        responses={200: CartItemSerializer}
    ),
    destroy=extend_schema(
        summary="Remove an item from the cart",
        description="Removes a product from the cart..",
        responses={204: {"description": "Item deleted successfully"}}
    ),
)
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
    