from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    commenting_user = serializers.StringRelatedField()
    comment_parent = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(), required=False, allow_null=True 
    )

    class Meta:
        model = Comment
        fields = ['id', 'product', 'commenting_user', 'comment_text', 'comment_parent']
        extra_kwargs = {
            "product": {"required": False}  
        }
