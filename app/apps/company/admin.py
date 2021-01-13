from django.contrib import admin

# Register your models here.
from company.models import *


class CompanyAdmin(admin.ModelAdmin):
    pass


class TaxOfficeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company, CompanyAdmin)
admin.site.register(TaxOffice, TaxOfficeAdmin)
