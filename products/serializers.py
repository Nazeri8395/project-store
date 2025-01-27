from rest_framework import serializers
from .models import Brand, Feature, FeatureValue, Product, ProductGroup

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'image_name', 'price', 'product_group', 'brand', 'is_active', ] 
        
class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = ['group_title', 'image_name', 'description', 'is_active', 'group_parent']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"
        
class FeatureValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureValue
        fields = ['id', 'value_title']  

class FeatureSerializer(serializers.ModelSerializer):
    feature_values = FeatureValueSerializer(many=True) 

    class Meta:
        model = Feature
        fields = ['id', 'feature_name', 'feature_values']     