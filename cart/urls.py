from django.urls import path, include
from  . import views
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers


router = SimpleRouter()
router.register("carts",views.CartViewSet, basename="carts")
cart_items_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_items_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + cart_items_router.urls
