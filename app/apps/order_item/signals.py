from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderItem


@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def populate_order_total_amount(sender, instance, **kwargs):
    order = instance.order
    order.calculate_total_amount()


# def populate_order_total_amount_2(sender, instance, **kwargs):
#     order = instance.order
#     order.calculate_total_amount()
