from django.apps import AppConfig


class OrderConfig(AppConfig):
    name = 'order_item'

    def ready(self):
        from .signals import populate_order_total_amount
