from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from products.models import Product
from products.serializers import ProductSerializer

class ProductSearchView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            products = Product.objects.filter(
                Q(product_name__icontains=query) | Q(description__icontains=query)  
            )
        else:
            products =Product.objects.none()

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
