from django.urls import path
from .views import CreateCommentView, ProductCommentsView

urlpatterns = [
    path('add/<int:product_id>/', CreateCommentView.as_view(), name='add_comment'),
     path('product/<int:product_id>/', ProductCommentsView.as_view(), name='product-comments'),
]
