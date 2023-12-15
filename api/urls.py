from django.urls import path, include
import api.views
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('categories', views.CategoryViewSet)
router.register('tags', views.TagViewSet)
router.register('product', views.ProductViewSet)
router.register('products-attribute', views.ProductAttributeViewSet)
router.register('products-image', views.ProductImageViewSet)
router.register('orders', views.OrderViewSet)
router.register('order-items', views.OrderItemViewSet)
router.register('stocks', views.StockViewSet)
router.register('stocks-image', views.StockImageViewSet)


urlpatterns = [
    path('auth/', include('api.auth.urls')),

    path('', include(router.urls))
]