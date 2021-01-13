import sys
import traceback

from apps.integration.services.sap.sap import SAP
from django.core.management.base import BaseCommand
from sentry_sdk import capture_exception

from address.models import Township


class Command(BaseCommand):
    help = 'Add accounting_id to townships'

    def handle(self, *args, **options):
        try:
            sap = SAP()
            sap_location_list = sap.get_location_info_crm()['EXPORT'][
                'ES_OUTPUT']
            city_list = {i['BEZEI']: i for i in sap_location_list['REGION']}
            township_list = [i for i in sap_location_list['CITY_NO'] if
                             i['COUNTRY'] == 'TR']
            for t in Township.objects.all():
                city = t.city
                c_name = _c_name = city.name

                if "maraş" in c_name:
                    _c_name = "K.Maraş"
                elif "Mersin" in c_name:
                    _c_name = "İçel"

                if city_list.get(_c_name):
                    city_in_sap = city_list.get(_c_name)
                    if not city.data:
                        city.data = {}
                    city.data['sap_no'] = city_in_sap['BLAND']
                    city.save()
                    print(f"Şehir güncellendi, {city.name}")
                else:
                    continue

                sap_township = [i for i in township_list if
                                i['REGION'] == str(city.data['sap_no']) and i[
                                    'CITY_NAME'] == t.name.replace("i",
                                                                   "İ").upper()]
                if sap_township and len(sap_township) == 1:
                    township = sap_township[0]
                    sap_no = township['CITY_CODE']
                    if not t.data:
                        t.data = {}
                    t.data['sap_no'] = sap_no
                    t.save(get_poly=False)
                    print(f"Township güncellendi, {t.name}")
                else:
                    print(
                        f"Birden fazla (ya da 0) sonuç bulunduğu için güncellenemedi-> {t.name}")

        except Exception as e:
            capture_exception(e)
            self.stdout.write(
                '\n'.join(traceback.format_exception(*(sys.exc_info()))))
