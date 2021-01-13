from django.db import models
from django.utils.translation import ugettext_lazy as _t
from core.models import CoreModel


class OrderItem(CoreModel):
    order = models.ForeignKey(
        "order.Order",
        on_delete=models.CASCADE,
        verbose_name=_t("Order"),
        related_name="orderitem"
    )
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.PROTECT,
        verbose_name=_t("Product"),
        related_name="product"
    )
    # 24
    quantity = models.FloatField(default=0, verbose_name="Sipariş Miktarı")

    # 1
    package_count = models.FloatField(
        verbose_name=_t("Package Quantity"),
        null=True, blank=True,
        default=1
        # default ekle
    )  # package unit'in katları olmalı, önyüzde hallet
    # package unit / quantity

    ##### quantity ve koli adedi çift taraflı çalşsın
    # 2 * 12 = 24 -> 24 / 2 = 2

    # koli_sayisi = models.IntegerField(null=True, blank=True, verbose_name="Koli Sayısı")
    # # default boş,

    list_price = models.FloatField(default=0, verbose_name=_t("Selling Price"))
    # default -> selling_price 10 -> 15

    # list_price = models.FloatField(default=0, verbose_name="Liste Fiyatı")
    # expo_price = models.FloatField(default=0, verbose_name="Fuar Fiyatı")

    total_amount = models.FloatField(default=0, verbose_name="Toplam Tutar")
    total_amount_with_vat = models.FloatField(default=0,
                                              verbose_name="Toplam Tutar (KDVli)")

    def _json(self):
        return {
            "order": self.order,
            "product": self.product,
            "quantity": self.quantity,
            "package_count": self.package_count,
            "list_price": self.list_price,
            "total_amount": self.total_amount,
            "total_amount_with_vat": self.total_amount_with_vat,
        }

    def __str__(self):
        return f"{self.order.company.name} - {self.product}"
