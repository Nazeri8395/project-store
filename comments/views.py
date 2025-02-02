from rest_framework import generics, permissions
from .models import Comment
from rest_framework.exceptions import NotFound
from .models import Comment, Product
from .serializers import CommentSerializer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    post=extend_schema(
        description="Create a new comment for a specific product. Optionally, you can reply to an existing comment by providing the comment_parent ID.",
        request=CommentSerializer,
        responses={201: CommentSerializer},
    )
)
class CreateCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def perform_create(self, serializer):
        product_id = self.kwargs.get("product_id") 
        product = get_object_or_404(Product, id=product_id)
        
        comment_parent_id = self.request.data.get("comment_parent")
        comment_parent = None
        if comment_parent_id:
            comment_parent = get_object_or_404(Comment, id=comment_parent_id)
        
        serializer.save(
            commenting_user=self.request.user, 
            product=product, 
            approring_user=None,
            comment_parent=comment_parent
        )

      
@extend_schema_view(
    get=extend_schema(
        description="Retrieve all active comments for a specific product.",
        responses={200: CommentSerializer(many=True)},
    )
)
class ProductCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        product_id = self.kwargs['product_id'] 
        product = get_object_or_404(Product, id=product_id)
        return Comment.objects.filter(product=product, is_active=True).select_related('commenting_user')