from compare.serializers import ProductFeatureSerializer, ProductSerializer
from products.models import Product, ProductFeature
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  

class CompareView(APIView):

    def get(self, request):
        """Get a list of compared products """
        compare_list = request.session.get('compare_list', [])
        # products = Product.objects.filter(id__in=compare_list)
        
        # data = [{'id': p.id, 'name': p.product_name, 'price': p.price} for p in products]
        return Response({'compare_list': compare_list}, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        """Add product to comparison list """
        compare_list = request.session.get('compare_list', [])

        if product_id is None:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        if product_id not in compare_list:
            compare_list.append(product_id)
            request.session['compare_list'] = compare_list
            request.session.modified = True

        return Response({'message': 'Product added to compare list', 'compare_list': compare_list}, status=status.HTTP_200_OK)

    def delete(self, request, product_id):
        """ Remove product from comparison list """
        compare_list = request.session.get('compare_list', [])

        if product_id in compare_list:
            compare_list.remove(product_id)
            request.session['compare_list'] = compare_list
            request.session.modified = True

        return Response({'message': 'Product removed from compare list', 'compare_list': compare_list}, status=status.HTTP_200_OK)


class ListShowComparetView(APIView):
    def get(self, request, *args, **kwargs):
        compare_list = request.session.get('compare_list', [])
        products = Product.objects.filter(id__in=compare_list)
        serializer = ProductSerializer(products, many=True)

        return Response({"compare_items": serializer.data})

class GetFeaturesView(APIView):
    def get(self, request):
        """ Get the features of the compared products """
        compare_list = request.session.get('compare_list', [])
        
        features = ProductFeature.objects.filter(product_id__in=compare_list)
        features_data = ProductFeatureSerializer(features, many=True).data

        return Response({"features": features_data}, status=200)