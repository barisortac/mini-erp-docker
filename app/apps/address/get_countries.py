import requests
import json


class RestCountryApi:
    BASE_URI = 'https://restcountries.eu/rest/v1'

    def get_country_list(self, resource, term=''):
        if term and not resource.endswith("="):
            # add the forward slash only when there is a term
            # and it is not specifying the value part of a query string
            term = "/{}".format(term)

        uri = "{}{}{}".format(self.BASE_URI, resource, term)

        response = requests.get(uri)
        if response.status_code == 200:
            result_dict = {}  # will be return
            data = json.loads(response.text)  # parse json to dict
            if type(data) == list:
                for country_data in data:  # in case it is a list create python list with country instances
                    # print(country_data['name'], country_data['alpha2Code'])
                    name = country_data['name']
                    code = country_data['alpha2Code']
                    # result_dict.update()
                    result_dict[code] = name
            else:
                return False
            return result_dict
        elif response.status_code == 404:
            raise requests.exceptions.InvalidURL
        else:
            raise requests.exceptions.RequestException

    def get_countrys(self):
        resource = '/all'
        return self.get_country_list(resource)

    def insert(self):
        countrys_codes = self.get_countrys()

        from address.models import Country

        for c in countrys_codes:
            co, cr = Country.objects.get_or_create(name=countrys_codes[c])
            co.code = c
            co.save()

        return True
