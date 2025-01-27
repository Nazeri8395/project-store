from django.urls import path
from .views import CheapProductsView

urlpatterns = [
    path('cheap-products/', CheapProductsView.as_view(), name='cheap-products'),
]
