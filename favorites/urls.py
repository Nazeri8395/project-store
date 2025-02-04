from django.urls import path
from .views import ToggleFavoriteView

urlpatterns = [
    path("toggle-favorite/<int:product_id>/", ToggleFavoriteView.as_view(), name="toggle-favorite"),
]
