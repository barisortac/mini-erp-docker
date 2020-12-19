from django.db import models
from company.models import PaymentTypeEnum
from core.enums import OrderStateEnum, DeliveryTypeEnum
from core.models import CoreModel


class Offer(CoreModel):
    barcode_no = models.CharField(max_length=128, null=True, blank=True, verbose_name="Barkod No")
    # product
    order_date = models.DateTimeField(null=True, blank=True, verbose_name='Sipariş Tarihi')
    company = models.ForeignKey(
        "company.Company",
        on_delete=models.PROTECT,
        verbose_name="Firma"
    )
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.PROTECT,
        verbose_name="Ürün"
    )
    quantity = models.FloatField(default=0, verbose_name="Sipariş Miktarı")
    koli_adedi = models.IntegerField(null=True, blank=True, verbose_name="Koli Adedi")
    koli_sayisi = models.IntegerField(null=True, blank=True, verbose_name="Koli Sayısı")
    special_price = models.FloatField(default=0, verbose_name="Özel Fiyat")
    delivery_type = models.CharField(
        max_length=32, verbose_name='Teslimat Türü',
        choices=DeliveryTypeEnum.choose_list(),
        null=True, blank=True
    )
    delivery_date = models.DateTimeField(null=True, blank=True, verbose_name="Teslim Tarihi")
    payment_type = models.CharField(
        max_length=32, verbose_name='Tahsilat Türü',
        choices=PaymentTypeEnum.choose_list(),
        null=True, blank=True
    )
    note = models.CharField(max_length=256, null=True, blank=True, verbose_name="Not")
    list_price = models.FloatField(default=0, verbose_name="Liste Fiyatı")
    expo_price = models.FloatField(default=0, verbose_name="Fuar Fiyatı")
    state = models.CharField(
        max_length=32, verbose_name='Ödeme Şekli',
        choices=OrderStateEnum.choose_list(),
        null=True, blank=True
    )
    total_amount = models.FloatField(default=0, verbose_name="Liste Fiyatı")


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
        return f"{self.company} - {self.product}"
