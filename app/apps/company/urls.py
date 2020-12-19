from django.urls import path

from company.views import *

urlpatterns = [
    path('', company_list, name="company-list"),
    path('list/', CompanyListJson.as_view(), name="company-list-json"),
    path('create/', CompanyCreateView.as_view(), name='create-company'),
    path('update/<int:pk>', CompanyUpdateView.as_view(), name='update-company'),
    path('read/<int:pk>', CompanyReadView.as_view(), name='read-company'),
    path('delete/<int:pk>', CompanyDeleteView.as_view(), name='delete-company'),

    path('tax-office', tax_office_list, name="tax-office-list"),
    path('tax-office/list/', TaxOfficeListJson.as_view(), name='tax-office-list-json'),
    path('tax-office/create/', TaxOfficeCreateView.as_view(), name='create-tax-office'),
    path('tax-office/update/<int:pk>', TaxOfficeUpdateView.as_view(), name='update-tax-office'),
    path('tax-office/delete/<int:pk>', TaxOfficeDeleteView.as_view(), name='delete-tax-office'),
    path('tax-office/autocomplete/', TaxOfficeAutocomplete.as_view(),name='tax-office-autocomplete'),
]