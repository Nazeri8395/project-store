from django.urls import path
from .views import ScoreCreateView,ProductScoreView

urlpatterns = [
    path("score/<int:product_id>/", ScoreCreateView.as_view(), name="create-score"),
    path("product/<int:product_id>/score/", ProductScoreView.as_view(), name="product-score"),
]