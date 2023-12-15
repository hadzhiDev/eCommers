from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from core.models import (Tag, Category, Product, ProductImage, ProductAttribute,
                         OrderItem, Order, Stock, StockImage)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


class ProductAdminForm(forms.ModelForm):

    content = forms.CharField(widget=CKEditorUploadingWidget(), label='Контент')
    description = forms.CharField(widget=forms.Textarea, label='Описание', help_text='Просто описание')

    class Meta:
        model = Product
        fields = '__all__'


class ProductImageStackedInline(admin.TabularInline):

    model = ProductImage
    extra = 1


class ProductAttributeStackedInline(admin.TabularInline):

    model = ProductAttribute
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'is_published', 'get_image')
    list_display_links = ('id', 'name',)
    list_filter = ('category', 'tags', 'is_published',)
    search_fields = ('name', 'description', 'content',)
    readonly_fields = ('created_at', 'updated_at', 'get_big_image',)
    form = ProductAdminForm
    inlines = [ProductAttributeStackedInline, ProductImageStackedInline]

    @admin.display(description='Изображение')
    def get_image(self, item):
        if item.image:
            return mark_safe(f'<img src="{item.image.url}" width="150px">')
        return '-'

    @admin.display(description='Изображение')
    def get_big_image(self, item):
        if item.image:
            return mark_safe(f'<img src="{item.image.url}" width="100%">')
        return '-'


class OrderItemStackedInline(admin.StackedInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('price', 'total_price', 'created_at', 'updated_at',)


class OrderAdminForm(forms.ModelForm):

    address = forms.CharField(widget=forms.Textarea, label='Адрес')

    class Meta:
        model = Order
        fields = '__all__'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'total_price', 'status',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name', 'email', 'phone', 'address', 'home',)
    list_filter = ('created_at',)
    readonly_fields = ('total_price', 'created_at', 'updated_at',)
    inlines = (OrderItemStackedInline,)
    form = OrderAdminForm


class StockAdminForm(forms.ModelForm):

    address = forms.CharField(widget=forms.Textarea, label='Адрес')

    class Meta:
        model = Stock
        fields = '__all__'


class StockImageStackedInline(admin.TabularInline):

    model = StockImage
    extra = 1


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name', 'address',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at',)
    inlines = (StockImageStackedInline,)
    form = StockAdminForm


