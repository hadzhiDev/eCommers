from django.db import models
from django.core.exceptions import ValidationError

from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField

from utils.models import TimeStampAbstractModel


class Category(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    name = models.CharField('название', max_length=250, unique=True)

    def __str__(self):
        return f'{self.name}'


class Tag(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    name = models.CharField('название', max_length=255)

    def __str__(self):
        return f'{self.name}'


class Product(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ('-created_at',)

    name = models.CharField('название', max_length=100)
    description = models.CharField('описание', max_length=255, help_text='Просто описание')
    content = models.TextField('контент')
    category = models.ForeignKey('core.Category', models.PROTECT, verbose_name='категория',
                                 help_text='Выберите категорию')
    tags = models.ManyToManyField('core.Tag', verbose_name='теги')
    price = models.DecimalField('цена', max_digits=10, decimal_places=2, default=0.0)
    quantity = models.PositiveIntegerField('количество', default=1)
    stock = models.ForeignKey('core.Stock', models.CASCADE, 'products', verbose_name='склады')
    is_published = models.BooleanField('публичность', default=True)

    @property
    def image(self):
        if self.images.first():
            return self.images.first().image
        return None

    # def clean(self):
    #     if self.quantity == 0:
    #         print(self)
    #         self.delete()

    def __str__(self):
        return f'{self.name}'


class ProductImage(TimeStampAbstractModel):

    class Meta:
        verbose_name = 'изображение товара'
        verbose_name_plural = 'изображении товаров'
        ordering = ('-created_at',)

    product = models.ForeignKey('core.Product', models.CASCADE, 'images', verbose_name='товар')
    image = ResizedImageField('изображение', upload_to='product_images/', force_format='WEBP', quality=90)

    def __str__(self):
        return f'{self.product.name}'


class ProductAttribute(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'атрибут товара'
        verbose_name_plural = 'атрибуты товаров'
        ordering = ('-created_at',)

    name = models.CharField('название', max_length=50)
    value = models.CharField('значение', max_length=50)
    product = models.ForeignKey('core.Product', models.CASCADE, 'attributes', verbose_name='товар')

    def __str__(self):
        return f'{self.name} - {self.value}'


class Order(TimeStampAbstractModel):

    WAITING = 'waiting'
    CANCELED = 'canceled'
    ON_DELIVERY = 'on_delivery'
    DELIVERED = 'delivered'

    ORDER_STATUS = (
        (WAITING, 'В ожидание'),
        (CANCELED, 'Отменено'),
        (ON_DELIVERY, 'Доставляется'),
        (DELIVERED, 'Доставлено')
    )
    name = models.CharField('имя и фамилия', max_length=140)
    email = models.EmailField('электронная почта')
    phone = PhoneNumberField('номер телефона')
    address = models.CharField('адрес', max_length=255)
    home = models.CharField('номер квартара или дома', max_length=150)
    status = models.CharField('статус', choices=ORDER_STATUS, default=WAITING, max_length=20)

    def __str__(self):
        return f'{self.name} - {self.email}'

    def clean(self):
        if len(self.name) < 3:
            raise ValidationError({'name': ['Name must be at least 3 characters']})

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    total_price.fget.short_description = 'Итоговая цена'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ('-created_at',)


class OrderItem(TimeStampAbstractModel):

    class Meta:
        verbose_name = 'заказ товара'
        verbose_name_plural = 'заказы товаров'
        ordering = ('-created_at',)

    order = models.ForeignKey('core.Order', models.CASCADE, 'items', verbose_name='заказ')
    product = models.ForeignKey('core.Product', models.PROTECT, verbose_name='товар')
    price = models.DecimalField('цена', max_digits=10, decimal_places=2, default=0.0)
    quantity = models.PositiveIntegerField('количество', default=1)

    def __str__(self):
        return f'{self.order} - {self.product}'

    def clean(self):
        prod = Product.objects.get(id=self.product.id)
        prod.quantity = prod.quantity - self.quantity
        prod.save()

    @property
    def total_price(self):
        return self.price * self.quantity
    total_price.fget.short_description = 'Итоговая цена'


class Stock(TimeStampAbstractModel):

    name = models.CharField('название', max_length=250, unique=True)
    address = models.CharField('адрес', max_length=255)

    @property
    def image(self):
        if self.images.first():
            return self.images.first().image
        return None

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'склад'
        verbose_name_plural = 'склады'
        ordering = ('-created_at',)


class StockImage(TimeStampAbstractModel):

    stock = models.ForeignKey('core.Stock', models.CASCADE, 'images', verbose_name='склад')
    image = ResizedImageField('изображение', size=[400, 600],
                              upload_to='stock_images/', force_format='WEBP', quality=90)

    def __str__(self):
        return f'{self.stock.name}'

    class Meta:
        verbose_name = 'изображение склада'
        verbose_name_plural = 'изображении складов'
        ordering = ('-created_at',)