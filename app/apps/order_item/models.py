from django.db import models
from core.models import CoreModel


class OrderItem(CoreModel):
    order = models.ForeignKey(
        "order.Order",
        on_delete=models.CASCADE,
        verbose_name="Sipariş",
        related_name="orderitem"
    )
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.PROTECT,
        verbose_name="Ürün",
        related_name="product"
    )
    #24
    quantity = models.FloatField(default=0, verbose_name="Sipariş Miktarı")

    #1
    package_count = models.FloatField(
        verbose_name="Koli Adedi",
        null=True, blank=True,
        default=1
        #default ekle
    ) # package unit'in katları olmalı, önyüzde hallet
    #package unit / quantity

    ##### quantity ve koli adedi çift taraflı çalşsın
    # 2 * 12 = 24 -> 24 / 2 = 2

    # koli_sayisi = models.IntegerField(null=True, blank=True, verbose_name="Koli Sayısı")
    # # default boş,

    list_price = models.FloatField(default=0, verbose_name="Satış Fiyatı")
    # default -> selling_price 10 -> 15

    # list_price = models.FloatField(default=0, verbose_name="Liste Fiyatı")
    # expo_price = models.FloatField(default=0, verbose_name="Fuar Fiyatı")

    total_amount = models.FloatField(default=0, verbose_name="Toplam Tutar")
    total_amount_with_vat = models.FloatField(default=0, verbose_name="Toplam Tutar (KDVli)")

    def _json(self):
        return {
            "order_date": self.order_date,
            "company": self.company,
            "product": self.product,
            "koli_adedi": self.koli_adedi,
            "special_price": self.special_price,
            "delivery_type": self.delivery_type,
            "delivery_date": self.delivery_date,
            "payment_type": self.payment_type,
            "note": self.note,
            "koli_sayisi": self.koli_sayisi,
            "list_price": self.list_price,
            "state": self.state,
        }

    def __str__(self):
        return f"{self.order.company.name} - {self.product}"
