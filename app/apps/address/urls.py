from django.urls import path

from address import views

urlpatterns = [
#     path('list/', views.address_list,
#          name='address-list'),
#
#     path('list/json/', views.address_list_json,
#          name='address-list-json'),
#
#     path('form/', views.address_form,
#          name='address-form'),
#
#     path('form/<str:pk>/', views.address_form,
#          name='address-form'),
#
#     path('township/autocomplete/', views.TownshipAutocomplete.as_view(),
#          name='township-autocomplete'),
#
#     path('township/filter/autocomplete/', views.TownshipFilterAutocomplete.as_view(),
#          name='township-filter-autocomplete'),
#
#     path('district/autocomplete/', views.DistrictAutocomplete.as_view(),
#          name='district-autocomplete'),
#
#     path('address/autocomplete/', views.AddressAutocomplete.as_view(),
#          name='address-autocomplete'),
#
    path('city/autocomplete/', views.CityAutocomplete.as_view(),
         name='city-autocomplete'),
#
#     path('state/autocomplete/', views.StateAutocomplete.as_view(),
#          name='state-autocomplete'),
#
]
