from django.dispatch import receiver
from django.db.models.signals import post_save

from core.models import OrderItem


@receiver(post_save, sender=OrderItem)
def order_item_post_save(sender, instance: OrderItem, created, *args, **kwargs):
    if created:
        product = instance.product
        instance.price = product.price
        instance.save()
