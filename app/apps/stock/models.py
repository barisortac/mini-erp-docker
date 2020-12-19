from django.db import models

from core.models import CoreModel


class Stock(CoreModel):
    number = models.IntegerField(default=0, verbose_name="Stok No", unique=True)
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.PROTECT,
        verbose_name="Ürün"
    )
    stock_quantity = models.IntegerField(default=0, verbose_name="Stok Miktarı")
    base_cost = models.FloatField(default=0, verbose_name="Ürün Tipi")


    def __str__(self):
        return f"{self.product.name} - {self.number}"
