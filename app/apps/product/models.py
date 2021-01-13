from django.core.validators import MinValueValidator
from django.db import models

from core.models import CoreModel


class ProductSize(CoreModel):
    olcu = models.CharField(max_length=128, verbose_name="Ölçü")
    bobin = models.FloatField(default=0, verbose_name="Bobin")
    kesim = models.FloatField(default=0, verbose_name="Kesim")
    sarim = models.FloatField(default=0, verbose_name="Sarım")
    metre = models.FloatField(default=0, verbose_name="Metre")
    sarim_adet_mt = models.CharField(max_length=128,
                                     verbose_name="Sarım Adet/Mt")
    koli_adeti = models.CharField(max_length=128, verbose_name="Sarım Adet/Mt")


class ProductType(CoreModel):
    """
    TERMAL 55 GR
    EKO TERMAL
    LAMİNE TERMAL
    KARTON TERMAL
    LAMİNE KARTON TERMAL
    OTOKOPY
    KUŞE ETİKET
    """
    name = models.CharField(max_length=128, verbose_name="Ürün Tipi")

    def __str__(self):
        return f"{self.name}"

    def _json(self):
        return f"{self.name}"


class Product(CoreModel):
    name = models.CharField(max_length=256, verbose_name="Ürün Adı")
    description = models.CharField(max_length=512, null=True, blank=True,
                                   verbose_name='Stok Açıklaması')
    # size = models.ForeignKey(
    #     ProductSize,
    #     on_delete=models.PROTECT,
    #     verbose_name="Stok Ölçüsü"
    # )

    # 24
    package_unit = models.FloatField(default=1, verbose_name="Ambalaj Birimi",
                                     validators=[MinValueValidator(
                                         0.0)])  # 10'lu ambalaj katları vs.
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.PROTECT,
        verbose_name="Cinsi",
        null=True,
        blank=True
    )
    buying_price = models.FloatField(default=0, verbose_name="Alış Fiyatı")

    # vat_rate ekle
    # vat_rate
    vat_rate = models.FloatField(default=1, verbose_name="KDV")
    selling_price = models.FloatField(default=0, verbose_name="Satış Fiyatı")

    def __str__(self):
        return f"{self.name}"

    def _json(self):
        return {
            "name": self.name,
            "description": self.description,
            "package_unit": self.package_unit,
            "product_type": self.product_type and self.product_type.name,
            "buying_price": self.buying_price,
            "vat_rate": self.vat_rate,
            "selling_price": self.selling_price,
        }
