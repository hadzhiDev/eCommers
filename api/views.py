from django.shortcuts import render
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.filters import ProductFilter
from api.paginations import SimpleResultPagination
from api.mixins import UltraModelViewSet
from api.serializers import CategorySerializer, TagSerializer, ProductSerializer, ReadProductSerializer, \
    CreateProductSerializer, ProductAttributeSerializer, ProductImageSerializer, OrderSerializer, CreateOrderSerializer, \
    OrderItemSerializer, ReadStockSerializer, RetrieveStockSerializer, CreateStockSerializer, StockSerializer, \
    StockImageSerializer
from api.permissions import IsOwner, IsSuperAdmin, IsOwnerForProduct

from core.models import Category, Product, Tag, ProductAttribute, ProductImage, Order, OrderItem, Stock, StockImage


class CategoryViewSet(UltraModelViewSet):
    queryset = Category.objects.all()
    pagination_class = SimpleResultPagination
    serializer_class = CategorySerializer
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']
    permission_classes_by_action = {
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'create': (IsAuthenticated,),
        'update': (IsAuthenticated,),
        'destroy': (IsAuthenticated,),
    }


class TagViewSet(UltraModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']
    permission_classes_by_action = {
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'create': (IsAuthenticated, IsSuperAdmin,),
        'update': (IsAuthenticated, IsSuperAdmin,),
        'destroy': (IsAuthenticated, IsSuperAdmin,),
    }


class ProductViewSet(UltraModelViewSet):
    queryset = Product.objects.all()
    serializer_classes = {
        'list': ReadProductSerializer,
        'update': ProductSerializer,
        'create': CreateProductSerializer,
        'retrieve': ReadProductSerializer,
    }
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['is_published', 'price']
    search_fields = ['name', 'description', 'content']
    filterset_class = ProductFilter
    permission_classes_by_action = {
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'create': (IsAuthenticated,),
        'update': (IsAuthenticated,),
        'destroy': (IsAuthenticated,),
    }


class ProductAttributeViewSet(UltraModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'value']
    filterset_fields = ['product']
    permission_classes_by_action = {
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'create': (IsAuthenticated,),
        'update': (IsAuthenticated, IsOwnerForProduct,),
        'destroy': (IsAuthenticated, IsOwnerForProduct,),
    }


class ProductImageViewSet(UltraModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['product']
    permission_classes_by_action = {
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'create': (IsAuthenticated,),
        'update': (IsAuthenticated, IsOwnerForProduct,),
        'destroy': (IsAuthenticated, IsOwnerForProduct,),
    }


class OrderViewSet(UltraModelViewSet):
    queryset = Order.objects.all()
    serializer_classes = {
        'list': OrderSerializer,
        'retrieve': OrderSerializer,
        'update': OrderSerializer,
        'create': CreateOrderSerializer,
    }
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at']
    search_fields = ['name', 'email', 'phone', 'address', 'home']
    filterset_fields = ['items__product']
    permission_classes_by_action = {
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'create': (AllowAny,),
        'update': (IsAuthenticated, IsSuperAdmin,),
        'destroy': (IsAuthenticated, IsSuperAdmin,),
    }


class OrderItemViewSet(UltraModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at', 'price', 'quantity']
    filterset_fields = ['product', 'order']
    permission_classes_by_action = {
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'create': (AllowAny,),
        'update': (IsAuthenticated, IsSuperAdmin,),
        'destroy': (IsAuthenticated, IsSuperAdmin,),
    }


class StockViewSet(UltraModelViewSet):
    queryset = Stock.objects.all()
    serializer_classes = {
        'list': ReadStockSerializer,
        'retrieve': RetrieveStockSerializer,
        'update': StockSerializer,
        'create': CreateStockSerializer,
    }
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at',]
    filterset_fields = ['address', ]
    permission_classes = (IsAuthenticated, IsSuperAdmin)


class StockImageViewSet(UltraModelViewSet):
    queryset = StockImage.objects.all()
    serializer_class = StockImageSerializer
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['stock']
    permission_classes = (IsAuthenticated, IsSuperAdmin)


