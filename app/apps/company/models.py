from django.db import models

# Create your models here.
from core.enums import PaymentTypeEnum
from core.models import CoreModel


class TaxOffice(CoreModel):
    name = models.CharField(max_length=128, verbose_name="Vergi Dairesi")

    def __str__(self):
        return f"{self.id} - {self.name}"


class Company(CoreModel):
    name = models.CharField(max_length=128, verbose_name="Firma Adı")
    code = models.CharField(max_length=64, null=True, blank=True,
                            verbose_name="Cari Kodu", unique=True)
    # customer = models.ForeignKey('customer.Customer', on_delete=models.PROTECT,verbose_name=_t('Customer'))
    city = models.ForeignKey(
        "address.City", default=None,
        on_delete=models.PROTECT,
        null=True, blank=True,
        verbose_name="Şehir"
    )
    district = models.ForeignKey(
        "address.Township", default=None,
        on_delete=models.PROTECT,
        null=True, blank=True,
        verbose_name="İlçe"
    )
    tax_office = models.ForeignKey(
        TaxOffice, default=None,
        on_delete=models.PROTECT,
        null=True, blank=True,
        verbose_name="Vergi Dairesi"
    )
    tax_number = models.IntegerField(null=True, blank=True,
                                     verbose_name="Vergi Numarası", unique=True)
    phone = models.CharField(max_length=32, null=True, blank=True,
                             verbose_name='Telefon Numarası')
    payment_type = models.CharField(
        max_length=32, verbose_name='Ödeme Şekli',
        choices=PaymentTypeEnum.choose_list(),
        null=True, blank=True
    )

    def _json(self):
        return {
            'name': self.name,
            'code': self.code,
            'city': self.city,
            'district': self.district,
            'tax_office': self.tax_office,
            'tax_number': self.tax_number,
            'phone': self.phone,
            'payment_type': self.payment_type,
            'created_at': self.created_at,
        }

    def __str__(self):
        return self.name
