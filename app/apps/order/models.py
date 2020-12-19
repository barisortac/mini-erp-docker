from datetime import datetime

from django.db import models
from django.db.models import Sum

from company.models import PaymentTypeEnum
from core.enums import OrderStateEnum, DeliveryTypeEnum, OrderTypeEnum
from core.models import CoreModel

# def get_list_price(id):
#     return

# class KoliAdedi(CoreModel):
#     adet = models.IntegerField(null=True, blank=True, verbose_name="Koli Adedi")

class Order(CoreModel):
    order_date = models.DateTimeField(null=True, blank=True, verbose_name='Sipariş Tarihi')
    company = models.ForeignKey(
        "company.Company",
        on_delete=models.PROTECT,
        verbose_name="Firma",
        related_name="company"
    )
    total_quantity = models.FloatField(default=0, verbose_name="Toplam Sipariş Sayısı")
    total_package_count = models.FloatField(default=0, verbose_name="Toplam Paket Sayısı")

    # delivery_type = models.CharField(
    #     max_length=32, verbose_name='Teslimat Türü',
    #     choices=DeliveryTypeEnum.choose_list(),
    #     null=True, blank=True
    # )
    # üretim kısmı gelince devreye alınacak, açık -> hazır -> satışa hazır

    delivery_date = models.DateTimeField(null=True, blank=True, verbose_name="Teslim Tarihi")
    # sipariş 1 ay sonra da olabilir, şimdi de

    payment_type = models.CharField(
        max_length=32, verbose_name='Tahsilat Türü',
        choices=PaymentTypeEnum.choose_list(),
        null=True, blank=True
    ) # t

    order_type = models.CharField(
        max_length=32, verbose_name='Sipariş Türü',
        choices=OrderTypeEnum.choose_list(),
        null=True, blank=True
    )

    note = models.CharField(max_length=256, null=True, blank=True, verbose_name="Not")

    # list_price = models.FloatField(default=0, verbose_name="Liste Fiyatı")
    # expo_price = models.FloatField(default=0, verbose_name="Fuar Fiyatı")
    state = models.CharField(
        max_length=32, verbose_name='Sipariş Durumu',
        choices=OrderStateEnum.choose_list(),
        null=True, blank=True,
        default=OrderStateEnum.OPEN
    )

    total_amount = models.FloatField(default=0, verbose_name="Toplam Tutar")
    # default = 0
    # quantity * list_price

    total_amount_with_vat = models.FloatField(default=0, verbose_name="Toplam Tutar (KDVli)")
    # 10 * 1,18

    discount = models.FloatField(default=0, verbose_name="İndirim")
    additional_discount = models.FloatField(default=0, verbose_name="Ek İndirim")
    # önce discount, sonra varsa additional discount
    # discountlar kdv katılmadan önce yapılır.

    # mf -> mal fazlası -> fiyat 0 olacak


    def _json(self):
        return {
            "order_date": self.order_date,
            "company": self.company and self.company.name,
            "delivery_date": self.delivery_date,
            "payment_type": self.payment_type,
            "order_type": self.order_type,
            "note": self.note,
            "state": self.state,
            "total_amount": self.total_amount,
            "total_amount_with_vat": self.total_amount_with_vat,
            "discount": self.discount,
            "additional_discount": self.additional_discount,
            "total_quantity": self.total_quantity,
            "total_package_count": self.total_package_count,
        }


    def api_json(self):
        return {
            "order_date": self.order_date and datetime.strftime(self.order_date, "%d.%m.%Y"),
            "delivery_date": self.delivery_date and datetime.strftime(self.delivery_date, "%d.%m.%Y"),
            # "order_date": str(self.order_date),
            # "delivery_date": str(self.delivery_date),
            "company": self.company and self.company.name,
            "payment_type": self.payment_type,
            "order_type": self.order_type,
            "note": self.note,
            "state": self.state,
            "total_amount": self.total_amount,
            "total_amount_with_vat": self.total_amount_with_vat,
            "discount": self.discount,
            "additional_discount": self.additional_discount,
            "total_quantity": self.total_quantity,
            "total_package_count": self.total_package_count,
        }

    def __str__(self):
        return f"{self.id} - {self.company}"

    def calculate_total_amount(self):
        order_items = self.orderitem.filter(is_active=True)
        total_amount = 0 or order_items.aggregate(Sum('total_amount'))['total_amount__sum']
        total_amount_with_vat = 0 or order_items.aggregate(Sum('total_amount_with_vat'))['total_amount_with_vat__sum']
        total_quantity = 0 or order_items.aggregate(Sum('quantity'))['quantity__sum']
        total_package_count = 0 or order_items.aggregate(Sum('package_count'))['package_count__sum']
        if total_amount:
            self.total_amount = round(float(total_amount), 2)
            self.total_amount_with_vat = round(float(total_amount_with_vat), 2)
            self.total_quantity = round(float(total_quantity), 2)
            self.total_package_count = round(float(total_package_count), 2)
            self.save()


