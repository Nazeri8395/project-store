from django.urls import path
from .views import (BrandsView, CheapProductsView, FeatureForFilter, LastProductsView, PopularGroup, 
                    PopularProductsGroupView, ProductByGroupView, 
                    ProductDetailsView, ProductGroupsView, RelatedProducts)

urlpatterns = [
    path('cheap-products/', CheapProductsView.as_view(), name='cheap-products'),
    path('last-products/', LastProductsView.as_view(), name='last-products'),
    path('popular-product-group/', PopularProductsGroupView.as_view(), name='popular-product-group'),
    path('product-details/<int:pk>/', ProductDetailsView.as_view(), name='productdetails'),
    path('related-products/<int:pk>/', RelatedProducts.as_view(), name='related-products'),
    path('productgroups/', ProductGroupsView.as_view(), name='productgroups'),
    path('product-of-group/<int:pk>', ProductByGroupView.as_view(), name='product-of-group'),
    path('popular-group', PopularGroup.as_view(), name='popular-group'),
    path('brand/<int:pk>', BrandsView.as_view(), name='brand'),
    path('feature-for-filter/<int:pk>', FeatureForFilter.as_view(), name='feature-for-filter'),
]
