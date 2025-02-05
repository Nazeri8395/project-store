from rest_framework import serializers
from products.models import ProductFeature, Feature, Product

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'feature_name']

class ProductFeatureSerializer(serializers.ModelSerializer):
    feature = FeatureSerializer(read_only=True) 

    class Meta:
        model = ProductFeature
        fields = ['id', 'product', 'feature', 'value']

class ProductSerializer(serializers.ModelSerializer):
    features = ProductFeatureSerializer(source='productfeature_set', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'features']