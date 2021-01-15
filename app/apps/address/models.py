from django.db import models
# from django.contrib.gis.db import models as gis_models
# from django.contrib.gis.db.models.fields import PointField
# from django.contrib.gis.geos import Point
from django.utils.translation import ugettext_lazy as _t
from core.models import CoreModel


class Country(CoreModel):
    CACHE_KEY = "country"

    name = models.CharField(max_length=64, verbose_name=_t('Name'))
    code = models.CharField(max_length=16, verbose_name=_t('Code'))
    slot = models.IntegerField(default=1, verbose_name=_t('Slot'))

    default_country = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ["slot", "name"]

    def _json(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code
        }


class State(CoreModel):
    CACHE_KEY = "state"

    name = models.CharField(max_length=32, verbose_name=_t('Name'))
    code = models.CharField(max_length=16, verbose_name=_t('Code'))

    class Meta:
        ordering = ["name"]

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name


class City(CoreModel):
    CACHE_KEY = "city"

    CACHE_KEY = 'ci'
    CACHE_KEY_BULK = 'cib'

    name = models.CharField(max_length=128, verbose_name=_t('Name'))
    country = models.ForeignKey(
        'Country', on_delete=models.PROTECT, verbose_name=_t('Country'))

    #  is_active = models.BooleanField(default=True, verbose_name=_t('Is Active'))
    slot = models.IntegerField(default=1, verbose_name=_t('Slot'))
    use_in = models.BooleanField(default=False, verbose_name=_t('Use In'))

    class Meta:
        ordering = ['slot', 'name']

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name

    def _json(self):
        return {
            'id': self.id,
            'name': self.name,
            # 'country': self.country.name,
            # 'country_id': self.country_id
        }

    @staticmethod
    def _bulk_json():
        data = City._get_cache(City.CACHE_KEY_BULK)

        if data:
            return data
        else:
            data = []

        for c in City.objects.filter(is_active=True):
            data.append(c._json())

        City._set_cache(City.CACHE_KEY_BULK, data)

        return data


class Township(CoreModel):
    CACHE_KEY = "township"

    city = models.ForeignKey(
        'City', on_delete=models.PROTECT, verbose_name=_t('City'))
    name = models.CharField(max_length=128, verbose_name=_t('Name'))

    #  is_active = models.BooleanField(default=True, verbose_name=_t('Is Active'))
    # poly = gis_models.GeometryField(null=True, blank=True, spatial_index=True)

    CACHE_KEY = 'tw'
    CACHE_KEY_BULK = 'twb'

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % self.name

    def __str__(self):
        return self.name

    def get_place_id(self):
        return int(self.data.get("place_id", 0))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def _json(self):
        return {
            'id': self.id,
            'name': self.name,
            'city_id': self.city_id,
            'city': self.city.name,
            'is_active': self.is_active
        }


class District(CoreModel):
    CACHE_KEY = "district"

    township = models.ForeignKey('Township', on_delete=models.PROTECT,
                                 verbose_name=_t('Township'))
    name = models.CharField(max_length=128, verbose_name=_t('Name'))

    CACHE_KEY_BULK = 'dtb'

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def city(self):
        return self.township.city.name

    def _json(self):
        return {
            'id': self.id,
            'name': self.name,
            'township': self.township.name,
            'township_id': self.township_id,
            'city': self.township.city.name,
            'city_id': self.township.city.id,
            'is_active': self.is_active
        }


class Address(CoreModel):
    CACHE_KEY = "adress"

    address_title = models.CharField(max_length=512,
                                     verbose_name=_t('Address Title'))
    address = models.TextField()
    state = models.ForeignKey(
        State, on_delete=models.PROTECT, null=True, blank=True,
        verbose_name=_t('State'))
    city = models.ForeignKey(
        'City', on_delete=models.PROTECT, verbose_name=_t('City')
    )
    township = models.ForeignKey('Township', on_delete=models.PROTECT,
                                 verbose_name=_t('Township'))
    district = models.ForeignKey(
        'District', null=True, blank=True, on_delete=models.PROTECT,
        verbose_name=_t('District'))
    postal_code = models.CharField(max_length=10, blank=True, null=True,
                                   verbose_name=_t('Postal Code'))
    phone = models.CharField(max_length=32, verbose_name=_t('Phone'),
                             help_text=u'Örn: 5301234567')
    # dahili
    internal = models.CharField(
        max_length=64, verbose_name=u'Dahili', null=True, blank=True, )
    fax = models.CharField(
        max_length=64, help_text=u'Örn: 2122454545', null=True, blank=True,
        verbose_name=_t('Fax'))
    name = models.CharField(max_length=256, null=True, blank=True,
                            verbose_name=_t('Name'))
    identity_number = models.CharField(max_length=64, null=True, blank=True,
                                       verbose_name=_t('Identity Number'))

    tax_no = models.CharField(max_length=256, null=True, blank=True,
                              verbose_name=_t('Tax No'))
    tax_office = models.CharField(max_length=256, null=True, blank=True,
                                  verbose_name=_t('Tax Office'))
    # geom = PointField(null=True, blank=True, verbose_name=_t('Geom'))

    is_cancelled = models.BooleanField(default=False,
                                       verbose_name=_t('Is Cancelled'))
    cancelled_at = models.DateTimeField(null=True, blank=True,
                                        verbose_name=_t('Cancelled At'))

    def __unicode__(self):
        return u' %s - %s' % (self.id, self.address_title)

    def __str__(self):
        return self.address_title

    def get_address(self):
        return u'%s %s %s %s ' % (
            self.address, self.postal_code or '', self.township, self.city)

    def _json(self):
        return self._asdict()