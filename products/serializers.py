from rest_framework import serializers
from .models import Brand, Feature, FeatureValue, Product, ProductGroup

class ProductSerializer(serializers.ModelSerializer):
    user_score = serializers.SerializerMethodField()
    average_score = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "product_name", "description", "price", "is_active", "user_score", "average_score", "is_favorite"]

    def get_user_score(self, obj):
        """Get logged in user score from model"""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.get_user_score(request.user)
        return None

    def get_average_score(self, obj):
        """Get average product scores from model"""
        return obj.get_average_score()

    def get_is_favorite(self, obj):
        """Check if the user has added this product to favorites"""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.is_favorited_by(request.user)
        return False
    
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