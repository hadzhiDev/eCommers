from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from core.models import Category, Product, Tag, ProductImage, ProductAttribute, Order, OrderItem, StockImage, Stock


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'created_at')


class ImageForProductCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image',)


class AttributeForProductCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ('id', 'name', 'value',)


class ProductSerializer(WritableNestedModelSerializer):
    images = ImageForProductCreationSerializer(many=True)
    attributes = AttributeForProductCreationSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class CreateProductSerializer(WritableNestedModelSerializer):
    images = ImageForProductCreationSerializer(many=True)
    attributes = AttributeForProductCreationSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        attributes = validated_data.pop('attributes', [])
        product = super().create(validated_data)\

        for attribute in attributes:
            ProductAttribute.objects.create(product=product, **attribute)

        for image in images:
            ProductImage.objects.create(product=product, **image)

        return product


class ReadProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    tags = TagSerializer(many=True)
    # user = serializers.CharField(source='User.email')
    # user_id = serializers.IntegerField(source='user.id')
    image = serializers.SerializerMethodField()
    images = ImageForProductCreationSerializer(many=True)
    attributes = AttributeForProductCreationSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_image(self, product):
        request = self.context['request']
        if product.image:
            return request.build_absolute_uri(product.image.url)
        return None


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ItemForReadOrderSerializer(serializers.ModelSerializer):
    product = ReadProductSerializer(read_only=True)
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('product', 'price', 'quantity', 'total_price',)


class OrderSerializer(serializers.ModelSerializer):
    items = ItemForReadOrderSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        total_price = sum(item.total_price for item in instance.items.all())
        ret.setdefault('total_price', total_price)
        return ret


class ItemForCreateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity',)


class CreateOrderSerializer(serializers.ModelSerializer):
    items = ItemForCreateOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, attrs):
        if len(attrs['name']) < 3:
            raise serializers.ValidationError({
                'name': [
                    'Name must be at least 3 characters'
                ]
            })
        return attrs

    def validate_home(self, value):
        if len(value) > 3:
            raise serializers.ValidationError(['Home must be at least 3 characters'])
        return value

    def create(self, validated_data):
        items = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        for item in items:
            OrderItem.objects.create(**item, order=order)
        return order


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'


class ImageForStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockImage
        fields = ('id', 'image',)


class StockImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockImage
        fields = '__all__'


class ReadStockSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    images = ImageForStockSerializer(many=True)

    class Meta:
        model = Stock
        fields = '__all__'

    def get_image(self, stock):
        request = self.context['request']
        if stock.image:
            return request.build_absolute_uri(stock.image.url)
        return None


class RetrieveStockSerializer(serializers.ModelSerializer):
    products = ReadProductSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    images = ImageForStockSerializer(many=True)

    class Meta:
        model = Stock
        fields = '__all__'

    def get_image(self, stock):
        request = self.context['request']
        if stock.image:
            return request.build_absolute_uri(stock.image.url)
        return None


class CreateStockSerializer(serializers.ModelSerializer):
    images = ImageForStockSerializer(many=True)

    class Meta:
        model = Stock
        fields = '__all__'

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        stock = super().create(validated_data)
        for image in images:
            StockImage.objects.create(stock=stock, **image)
        return stock


class StockSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


