from django.urls import path
from .views import CompareView, ListShowComparetView, GetFeaturesView
from django.urls import path



urlpatterns = [
   path('', CompareView.as_view(), name='compare_list'),
   path('add/<int:product_id>/', CompareView.as_view(), name='add_to_compare'),
   path('remove/<int:product_id>/', CompareView.as_view(), name='remove_from_compare'),
   path('products/', ListShowComparetView.as_view(), name='products_compare'),
   path('product-feature/', GetFeaturesView.as_view(), name='product-feature'),
    
]
