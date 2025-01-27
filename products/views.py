from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

class CheapProductsView(APIView):
    def get(self, request):
        products = Product.objects.filter(is_active=True).order_by('price')[:3]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
