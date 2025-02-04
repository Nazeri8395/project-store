from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Favorite
from products.models import Product

class ToggleFavoriteView(APIView):
    def post(self, request, product_id):
        user = request.user
        product = get_object_or_404(Product, id=product_id)

        # Check if this product is in the wishlist or not
        favorite, created = Favorite.objects.get_or_create(product=product, favorite_user=user)

        if not created:
            # If it already exists, delete it (remove from favorites)
            favorite.delete()
            return Response({"message": "Removed from favorites"}, status=status.HTTP_200_OK)
        
        return Response({"message": "Added to favorites"}, status=status.HTTP_201_CREATED)
