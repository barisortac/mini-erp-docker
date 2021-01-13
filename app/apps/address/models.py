from django.db import models
# from django.contrib.gis.db import models as gis_models
# from django.contrib.gis.db.models.fields import PointField
# from django.contrib.gis.geos import Point
from django.utils.translation import ugettext_lazy as _t

from core.models import CoreModel


# from django.contrib.gis.geos import Polygon


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

    # def get_geojson(self, save=False, return_response=False):
    #     place_id = self.get_place_id()
    #     if place_id:
    #         url = f"https://nominatim.openstreetmap.org/details.php?place_id={place_id}&polygon_geojson=1&format=json"
    #         res = requests.get(url)
    #
    #         data = res.json()
    #         geojson = data["geometry"]
    #     else:
    #         url = f"https://nominatim.openstreetmap.org/search.php?q={self.city.name}+{self.name}&polygon_geojson=1&format=json"
    #         res = requests.get(url)
    #
    #         data = res.json()
    #         if return_response:
    #             return data
    #
    #         if data:
    #             if place_id:
    #                 for geo in data:
    #                     if geo["place_id"] == place_id:
    #                         geojson = geo.get("geojson")
    #                         break
    #             else:
    #                 if isinstance(data, list):
    #                     for d in data:
    #                         if d.get("geojson") and d.get("geojson").get("type")=="Polygon":
    #                             geojson = d.get("geojson")
    #                             break
    #                     else:
    #                         print(f"BU ŞEHİR-BÖLGE İÇİN POLYGON BULUNAMADI.. {self.city.name}, {self.name}")
    #                         return False
    #                 else:
    #                     geojson = data[0].get("geojson")
    #
    #
    #     if save and data:
    #         coords = geojson["coordinates"]
    #         if len(coords) > 1:
    #             try:
    #                 max_list = []
    #                 for c in coords:
    #                     max_list.append(len(c[0]))
    #                 max_index = max_list.index(max(max_list))
    #                 new_coords = coords[max_index][0]
    #             except Exception as e:
    #                 print(e)
    #                 raise e
    #         else:
    #             new_coords = coords[0]
    #
    #         if not len(new_coords) >= 4:
    #             print(
    #                 f"BU ŞEHİR-BÖLGE NİN POLYGON OLUŞTURMAK İÇİN "
    #                 f"YETERLİ SAYIDA NOKTASI YOK (EN AZ 4 OLMALI, "
    #                 f"BURDA {len(new_coords)}).. {self.city.name}, {self.name}"
    #             )
    #             return False
    #
    #         self.poly = Polygon(new_coords)
    #         self.save(update_fields=["poly"], get_poly=False)
    #
    #     return geojson

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # if get_poly:
        #     self.get_geojson(save=True)

    def _json(self):
        return {
            'id': self.id,
            'name': self.name,
            'city_id': self.city_id,
            'city': self.city.name,
            'is_active': self.is_active
        }

    @staticmethod
    def _bulk_json(city_id):
        data = Township._get_cache(Township.CACHE_KEY_BULK + city_id)
        if data:
            return data
        else:
            data = []

        for c in Township.objects.filter(is_active=True, city_id=city_id):
            data.append(c._json())

        Township._set_cache(Township.CACHE_KEY_BULK + city_id, data)

        return data

    # @staticmethod
    # def get_by_point(lon: float, lat: float):
    #     return Township.objects.filter(is_active=True, poly__contains=Point(lon, lat)).first()


class District(CoreModel):
    CACHE_KEY = "district"

    township = models.ForeignKey('Township', on_delete=models.PROTECT,
                                 verbose_name=_t('Township'))
    name = models.CharField(max_length=128, verbose_name=_t('Name'))

    #  is_active = models.BooleanField(default=True, verbose_name=_t('Is Active'))
    # poly = gis_models.GeometryField(null=True, spatial_index=True, blank=True)

    CACHE_KEY = 'dt'
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

    # def get_geojson(self):
    #     url = f"https://nominatim.openstreetmap.org/search.php?q={self.township.city.name}+{self.township.name}+{self.name}&polygon_geojson=1&format=json"
    #     res = requests.get(url)
    #     print(f"url --> {url}")
    #     return res.json()

    @staticmethod
    def _bulk_json(township_id):
        data = District._get_cache(District.CACHE_KEY_BULK + township_id)

        if data:
            return data
        else:
            data = []

        for c in District.objects.filter(is_active=True,
                                         township_id=township_id):
            data.append(c._json())

        District._set_cache(District.CACHE_KEY_BULK + township_id, data)

        return data

    # @staticmethod
    # def get_by_point(lon: float, lat: float):
    #     return District.objects.filter(is_active=True, poly__contains=Point(lon, lat)).first()


class Address(CoreModel):
    CACHE_KEY = "adress"

    address_title = models.CharField(max_length=512,
                                     verbose_name=_t('Address Title'))
    address = models.TextField()
    # address2 = models.TextField(blank=True, null=True)
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

    #  first_name = models.CharField(max_length=100, null=True, blank=True)
    #  last_name = models.CharField(max_length=100, null=True, blank=True)
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

    def _asdict(self):
        dic = {}
        dic['address_title'] = self.address_title
        #  dic['first_name'] = self.first_name
        dic['name'] = self.name
        dic['address'] = self.address
        # dic['address2'] = self.address2 if self.address2 else ''
        dic['city'] = self.city.name
        dic['city_id'] = self.city_id
        dic['township'] = self.township.name
        dic['township_id'] = self.township_id
        dic['district'] = self.district.name if self.district else ''
        dic['district_id'] = self.district_id
        dic['postal_code'] = self.postal_code
        dic['phone'] = self.phone
        dic['country'] = self.city.country.name
        dic['internal'] = self.internal
        dic['fax'] = self.fax
        dic['tax_no'] = self.tax_no
        dic['tax_office'] = self.tax_office
        # dic['address_id'] = self.id
        dic['id'] = self.id

        return dic

    def api_json(self):
        data = self._asdict()
        title = data['address_title']
        del data['address_title']
        data['title'] = title
        # a1 = data['address']
        # a2 = data['address2']
        # del data['address']
        # del data['address2']
        # data['address'] = a1 + ' ' + a2

        return data

    def ashtml(self):
        html = ''
        html += '%s <br/>' % self.address_title
        html += '%s <br/>' % (self.name)
        html += '%s <br/>' % self.address
        # if self.address2:
        #     html += '%s <br/>' % self.address2
        if self.phone:
            html += '%s <br/>' % self.phone
        if self.township or self.city:
            html += '%s / %s <br/>' % (self.township.name, self.city.name)
        return html

    def astext(self):
        txt = ''
        txt += '%s' % self.address_title
        txt += '%s' % (self.name)
        txt += '%s' % self.address
        # if self.address2:
        #   txt += '%s' % self.address2
        if self.phone:
            txt += '%s' % self.phone
        if self.township or self.city:
            txt += '%s / %s' % (self.township.name, self.city.name)
        return txt

    def asinvoice(self):
        html = ''
        # html  += '%s %s <br/>' % (self.first_name, self.last_name)
        html += '%s ' % self.address_title
        html += '%s ' % self.address
        # if self.address2:
        #     html += '%s <br/>' % self.address2
        if self.phone:
            html += 'Tel: %s ' % self.phone
        if self.fax:
            html += 'Fax: %s ' % self.fax
        if self.city:
            html += '%s / %s ' % (
            self.township.name if self.township else '', self.city.name)
        return html
