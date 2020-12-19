from django.contrib import admin
from .models import (
    Country,
    State,
    City,
    Township,
    District,
    Address
)


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']
    autocomplete_fields = [
        'deleted_by',
        'created_by',
        'updated_by'
    ]


class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']
    autocomplete_fields = [
        'deleted_by',
        'created_by',
        'updated_by'
    ]


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'is_active', 'slot']
    search_fields = ['name', 'country__name']
    autocomplete_fields = [
        'deleted_by',
        'created_by',
        'country',
        'updated_by'
    ]


class TownshipAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'is_active']
    search_fields = ['name', 'city__name']
    autocomplete_fields = [
        'deleted_by',
        'created_by',
        'city',
        'updated_by'
    ]


class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'township', 'is_active']
    search_fields = ['name', 'township__name']
    autocomplete_fields = [
        'deleted_by',
        'created_by',
        'township',
        'updated_by'
    ]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        # 'first_name',
        # 'last_name',
        'name',
        'address_title',
        'address',
        'state',
        'city',
        'township',
        'district',
        'postal_code',
        'phone',
        'internal',
        'fax',
        'tax_no',
        'tax_office',
        'is_cancelled',
        'cancelled_at',
    ]
    search_fields = ['name', 'district__name', 'address_title',
                     'city__name', 'township__name']
    autocomplete_fields = [
        'deleted_by',
        'created_by',
        'updated_by',
        'city',
        'township',
        'district',
        'state',
    ]


admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Township, TownshipAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Address, AddressAdmin)
