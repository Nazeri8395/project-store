from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Brand, Feature, Product, ProductGroup
from .serializers import BrandSerializer, FeatureSerializer, ProductGroupSerializer, ProductSerializer
from django.db.models import Q, Count, Min, Max
from django.shortcuts import get_object_or_404

#---------------------  cheapest products  ------------------------------
@extend_schema(
    summary="Get the cheapest products",
    description="This API returns the cheapest active products.",
    responses={200: ProductSerializer}
)
class CheapProductsView(APIView):
    def get(self, request):
        products = Product.objects.filter(is_active=True).order_by('price')[:3]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#---------------------  Latest products  ------------------------------
@extend_schema(
    summary="Get the latest products",
    description="This API returns the most recent active products.",
    responses={200: ProductSerializer}
)
class LastProductsView(APIView):
    def get(self, request):
        products = Product.objects.filter(is_active=True).order_by('-published_date')[:3]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#---------------------  Popular categories  ------------------------------
@extend_schema(
    summary="Get popular product categories",
    description="This API returns the most popular product groups.",
    responses={200: ProductGroupSerializer}
)
class PopularProductsGroupView(APIView):
    def get(self, request):
        product_groups = ProductGroup.objects.filter(Q(is_active=True)).annotate(count=Count("product_of_groups")).order_by('-count')[:1]
        serializer = ProductGroupSerializer(product_groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#---------------------  Product details  ------------------------------
@extend_schema(
    summary="Get product details",
    description="This API returns complete information about a specific product..",
    responses={
        200: ProductSerializer,
        404: {"description": "این کالا غیرفعال است."}
    }
)
class ProductDetailsView(APIView):
    def get(self,request, pk):
        product= get_object_or_404(Product,pk=pk)
        if product.is_active:
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "این کالا غیرفعال است."}, 
                status=status.HTTP_404_NOT_FOUND)

#--------------------  Related products  -----------------------------
@extend_schema(
    summary="Get related products",
    description="This API returns products related to the selected product..",
    responses={200: ProductSerializer}
)
class RelatedProducts(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk') 
        current_product = get_object_or_404(Product, pk=pk)
        related_products = []
        for group in current_product.product_group.all():
            related_products.extend(Product.objects.filter (
                                        Q(is_active=True) & 
                                        Q(product_group=group) & 
                                        ~Q(pk=current_product.id)
                                    ))
        serializer = ProductSerializer(related_products, many=True)    
        return Response(serializer.data, status=status.HTTP_200_OK)

#--------------------  List of all product groups  -----------------------------
@extend_schema(
    summary="Get a list of all product groups",
    description="This API returns a list of all active product groups..",
    responses={200: ProductGroupSerializer}
)
class ProductGroupsView(APIView):
    def get(self, request, *args, **kwargs):
        product_groups = ProductGroup.objects.filter(Q(is_active=True)).annotate(count=Count("products"))
        serializer = ProductGroupSerializer(product_groups, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

#--------------------  List of products for each group  -----------------------------
@extend_schema(
    summary="Receive products from the selected group",
    description="This API returns products of a specific group along with price analysis..",
    responses={200: ProductSerializer}
)
class ProductByGroupView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        curent_group = get_object_or_404(ProductGroup, pk=pk)
        products = Product.objects.filter(Q(is_active=True) & Q(product_group=curent_group))
        res_aggre = products.aggregate(min=Min("price"),max=Max("price"))
        serializer = ProductSerializer(products, many=True)
        
        return Response({
            "products": serializer.data,
            "aggregation": res_aggre
        }, status=status.HTTP_200_OK)

#--------------------  Popular categories  -----------------------------
@extend_schema(
    summary="Get best-selling categories",
    description="This API returns the best-selling product categories..",
    responses={200: ProductGroupSerializer}
)
class PopularGroup(APIView):
    def get(self, request):
        product_group = ProductGroup.objects.annotate(count= Count("product_of_groups")).filter(
            Q(is_active=True) & ~Q(count=0)).order_by('-count')
        serializer = ProductGroupSerializer(product_group, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
#--------------------  List of brands for filters  -----------------------------
@extend_schema(
    summary="Get product brands for filters",
    description="This API returns a list of active product brands for the selected group.",
    responses={200: BrandSerializer}
)
class BrandsView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        product_group = get_object_or_404(ProductGroup,pk=pk)
        brand = Brand.objects.filter(
            product_of_brand__product_group=product_group,
            product_of_brand__is_active=True
        ).annotate(
            count=Count("product_of_brand")
        ).order_by("-count")  
        serializer = BrandSerializer(brand,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#--------------------  List of features of the selected group  -----------------------------
class FeatureForFilter(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        product_group = get_object_or_404(ProductGroup,pk=pk)
        feature_list = product_group.feature_of_group.prefetch_related('feature_values')  
        
        serializer = FeatureSerializer(feature_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)