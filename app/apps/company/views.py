# import traceback
# import sys
# from dal import autocomplete
# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponseRedirect, JsonResponse
# from django.utils.translation import ugettext_lazy as _t
# from django.views.decorators.csrf import csrf_exempt
# from django.db import transaction
# from django.contrib import messages
# from django.urls import reverse
# from django.contrib.auth.decorators import login_required
#
# # from address.models import Address
# # from sky_services.log import LogService
# # from .models import Company, ParentCompany, CompanyAddress
# # from .forms import CompanyForm, CompanyAddressForm, ParentCompanyForm
#
#
# @login_required
# def company_list(request):
#     context = {
#         'title': _t('Company List'),
#         'legend': _t('Company List')
#     }
#     return render(request, 'company/company_list.html', context)
#
#
# @login_required
# @csrf_exempt
# def company_list_json(request):
#     post = request.POST
#     query = post.get("search[value]")
#     start = abs(int(post.get("start", 0)))
#     size = abs(int(post.get("length", 10)))
#     draw = abs(int(post.get("draw", 1)))
#
#     columns = [
#         'parent',
#         'legal_name',
#         'tax_office',
#         'tax_no',
#         'code',
#         'external_code',
#         'payment_term',
#         'commission_rate',
#         'is_approved',
#         'is_blocked',
#     ]
#
#     order_by = post.get('order[0][column]')
#     if order_by:
#         order_by = columns[int(order_by)]
#         order_by_dir = post.get('order[0][dir]')
#         order_by_dir = order_by_dir == 'desc' and '-' or ''
#         order_by = "{}{}".format(
#             order_by_dir, order_by
#         )
#
#     end = int(start) + int(size)
#
#     company = Company.objects.filter().order_by("-id")
#
#     if query:
#         company = company.filter(legal_name__icontains=query)
#
#     if order_by:
#         company = company.order_by(order_by)
#
#     total_count = company.count()
#
#     company = company[start:end]
#
#     datas = []
#     if company:
#         for c in company:
#             datas.append((c.json(c.id)))
#
#     data = {
#         "data": datas,
#         "recordsTotal": total_count,
#         "recordsFiltered": total_count,
#         "draw": draw
#     }
#
#     return JsonResponse(data)
#
#
# @login_required
# @has_permission(permissions=["company_menu", "company_menu_readonly"])
# def company_form(request, pk=None):
#     post = request.POST
#     address = None
#     if pk:
#         obj = get_object_or_404(Company, pk=pk)
#         # get address
#         try:
#             address = CompanyAddress.objects.get(
#                 company_id=pk
#             ).address
#         except Exception:
#             pass
#     else:
#         obj = Company()
#
#     if post:
#         form = CompanyForm(
#             post, request.FILES, instance=obj, prefix="main",
#             user=request.user, current_address=address
#         )
#
#         if form.is_valid():
#             log = LogService()
#             try:
#                 with transaction.atomic():
#                     obj = form.save()
#
#                     if not pk:
#                         messages.success(
#                             request, _t("{} Company created").format(
#                                 obj.legal_name
#                             )
#                         )
#                         action = "company create"
#                     else:
#                         messages.success(
#                             request, _t("{} Company updated").format(
#                                 obj.legal_name
#                             )
#                         )
#                         action = "company update"
#
#                     data = {
#                         "data": obj._json(),
#                         "description": f"{request.user.username}: {_t('{} {}').format(obj.legal_name, action)}",
#                         "user_id": request.user.id,
#                         "model": "Company",
#                         "model_id": str(obj.id),
#                         "action": action
#                     }
#                     data['data']['sky_user_name'] = request.user.username
#                     log.push_data(data=data, request=request)
#
#                     return HttpResponseRedirect(
#                         reverse("company-list"))
#
#             except Exception as e:
#                 traceback.print_exc(file=sys.stdout)
#                 messages.error(request, str(e))
#     else:
#         form = CompanyForm(
#             instance=obj, prefix="main",
#             user=request.user, current_address=address
#         )
#
#     context = {
#         "form": form,
#         "title": _t("Company Form"),
#     }
#
#     return render(request, "company/form.html", context)
#
#
# class CompanyAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             return Company.objects.none()
#
#         qs = Company.objects.filter()
#
#         if self.q:
#             qs = qs.filter(legal_name__istartswith=self.q)
#
#         return qs
#
#
# class ParentAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             return ParentCompany.objects.none()
#
#         qs = ParentCompany.objects.filter()
#
#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)
#
#         return qs
#
#
# @login_required
# @has_permission(permissions=["company_menu", "company_menu_readonly"])
# def company_address_list(request):
#     context = {
#         'title': _t('Company Address List'),
#         'legend': _t('Company Address List')
#     }
#     return render(request, 'company/company_address.html', context)
#
#
# @login_required
# @csrf_exempt
# @has_permission(permissions=["company_menu", "company_menu_readonly"])
# def company_address_list_json(request):
#     post = request.POST
#     query = post.get("search[value]")
#     start = abs(int(post.get("start", 0)))
#     size = abs(int(post.get("length", 10)))
#     draw = abs(int(post.get("draw", 1)))
#
#     columns = [
#         'company',
#         'address',
#         'is_default',
#     ]
#
#     order_by = post.get('order[0][column]')
#     if order_by:
#         order_by = columns[int(order_by)]
#         order_by_dir = post.get('order[0][dir]')
#         order_by_dir = order_by_dir == 'desc' and '-' or ''
#         order_by = "{}{}".format(
#             order_by_dir, order_by
#         )
#
#     end = int(start) + int(size)
#
#     company_address = CompanyAddress.objects.filter().order_by("-id")
#
#     if query:
#         company_address = company_address.filter(company__legal_name__icontains=query)
#
#     if order_by:
#         company_address = company_address.order_by(order_by)
#
#     total_count = company_address.count()
#
#     company_address = company_address[start:end]
#
#     datas = []
#     #TODO: convert json to _json
#     if company_address:
#         for c in company_address:
#             datas.append((c._json()))
#
#     data = {
#         "data": datas,
#         "recordsTotal": total_count,
#         "recordsFiltered": total_count,
#         "draw": draw
#     }
#
#     return JsonResponse(data)
#
#
# @login_required
# @has_permission(permissions=["company_menu", "company_menu_readonly"])
# def company_address_form(request, pk=None):
#     post = request.POST
#
#     if pk:
#         obj = get_object_or_404(CompanyAddress, pk=pk)
#     else:
#         obj = CompanyAddress()
#
#     if post:
#         form = CompanyAddressForm(
#             post, request.FILES, instance=obj, prefix="main",
#             user=request.user
#         )
#
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     obj = form.save()
#
#                     if not pk:
#                         messages.success(
#                             request, _t("{} Company Address created").format(
#                                 obj.company
#                             )
#                         )
#                     else:
#                         messages.success(
#                             request, _t("{} Company Address updated").format(
#                                 obj.company
#                             )
#                         )
#                     return HttpResponseRedirect(
#                         reverse("company-address-list"))
#
#             except Exception as e:
#                 body = '\n'.join(traceback.format_exception(*(sys.exc_info())))
#                 messages.error(request, str(e))
#     else:
#         form = CompanyAddressForm(
#             instance=obj, prefix="main",
#             user=request.user
#         )
#
#     context = {
#         "form": form,
#         "title": _t("Company Address Form"),
#     }
#
#     return render(request, "company/form.html", context)
#
#
# @login_required
# @has_permission(permissions=["company_menu", "company_menu_readonly"])
# def parent_company_list(request):
#     context = {
#         'title': _t('Parent Company List'),
#         'legend': _t('Parent Company List')
#     }
#     return render(request, 'company/parent_company_list.html', context)
#
#
# @login_required
# @csrf_exempt
# @has_permission(permissions=["company_menu", "company_menu_readonly"])
# def parent_company_list_json(request):
#     post = request.POST
#     query = post.get("search[value]")
#     start = abs(int(post.get("start", 0)))
#     size = abs(int(post.get("length", 10)))
#     draw = abs(int(post.get("draw", 1)))
#
#     columns = [
#         'name',
#     ]
#
#     order_by = post.get('order[0][column]')
#     if order_by:
#         order_by = columns[int(order_by)]
#         order_by_dir = post.get('order[0][dir]')
#         order_by_dir = order_by_dir == 'desc' and '-' or ''
#         order_by = "{}{}".format(
#             order_by_dir, order_by
#         )
#
#     end = int(start) + int(size)
#
#     parent_company = ParentCompany.objects.filter().order_by("-id")
#
#     if query:
#         parent_company = parent_company.filter(company__legal_name__icontains=query)
#
#     if order_by:
#         parent_company = parent_company.order_by(order_by)
#
#     total_count = parent_company.count()
#
#     parent_company = parent_company[start:end]
#
#     datas = []
#     # TODO: convert json to _json
#     if parent_company:
#         for c in parent_company:
#             datas.append((c.json(c.id)))
#
#     data = {
#         "data": datas,
#         "recordsTotal": total_count,
#         "recordsFiltered": total_count,
#         "draw": draw
#     }
#
#     return JsonResponse(data)
#
#
# @login_required
# @has_permission(permissions=["company_menu", "company_menu_readonly"])
# def parent_company_form(request, pk=None):
#     post = request.POST
#
#     if pk:
#         obj = get_object_or_404(ParentCompany, pk=pk)
#     else:
#         obj = ParentCompany()
#
#     if post:
#         form = ParentCompanyForm(
#             post, request.FILES, instance=obj, prefix="main",
#             user=request.user
#         )
#
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     obj = form.save()
#
#                     if not pk:
#                         messages.success(
#                             request, _t("{} Parent Company created").format(
#                                 obj.name
#                             )
#                         )
#                     else:
#                         messages.success(
#                             request, _t("{} Parent Company updated").format(
#                                 obj.name
#                             )
#                         )
#                     return HttpResponseRedirect(
#                         reverse("parent-company-list"))
#
#             except Exception as e:
#                 body = '\n'.join(traceback.format_exception(*(sys.exc_info())))
#                 messages.error(request, str(e))
#     else:
#         form = ParentCompanyForm(
#             instance=obj, prefix="main",
#             user=request.user
#         )
#
#     context = {
#         "form": form,
#         "title": _t("Parent Company Form"),
#     }
#
#     return render(request, "company/form.html", context)
import json
from datetime import datetime

from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)
from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django_datatables_view.base_datatable_view import BaseDatatableView

from company.models import Company, TaxOffice
from .forms import CompanyModelForm, TaxOfficeModelForm


@login_required
def company_list(request):
    return render(request, 'company/list_company.html')


class CompanyListJson(BaseDatatableView):
    model = Company

    columns = order_columns = [
        "id",
        "name",
        "code",
        "tax_office",
        "tax_number",
        "phone",
        "payment_type",
        "city",
    ]

    def filter_queryset(self, qs):
        sSearch = self.request.GET.get('search[value]', None)
        if sSearch:
            qs = qs.filter(
                Q(name__istartswith=sSearch) |
                Q(code__istartswith=sSearch) |
                Q(phone__istartswith=sSearch)
            )

        # more advanced example using extra parameters
        filter_city = self.request.GET.get('columns[7][search][value]', None)

        if filter_city:
            filter_city_id = json.loads(filter_city)
            if filter_city_id:
                q = Q(city__id=filter_city_id)
                qs = qs.filter(q)

        return qs

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'created_at':
            # escape HTML for security reasons
            # return escape('{0} {1}'.format(row.customer_firstname, row.customer_lastname))
            return datetime.strftime(row.created_at, "%Y-%m-%d %H:%M:%S")
        else:
            return super(CompanyListJson, self).render_column(row, column)


class Index(generic.ListView):
    model = Company
    context_object_name = 'company'
    template_name = 'index.html'


################ COMPANY #####################
class CompanyCreateView(BSModalCreateView):
    template_name = 'company/create_company.html'
    form_class = CompanyModelForm
    success_message = 'Başarılı: firma oluşturuldu.'
    success_url = reverse_lazy('company-list')


class CompanyUpdateView(BSModalUpdateView):
    model = Company
    template_name = 'company/update_company.html'
    form_class = CompanyModelForm
    success_message = 'Başarılı: firma güncellendi.'
    success_url = reverse_lazy('company-list')


class CompanyReadView(BSModalReadView):
    model = Company
    template_name = 'company/read_company.html'


class CompanyDeleteView(BSModalDeleteView):
    model = Company
    template_name = 'company/delete_company.html'
    success_message = 'Başarılı: firma silindi.'
    success_url = reverse_lazy('company-list')


################ COMPANY #####################


################ TAX OFFICE #####################
@login_required
def tax_office_list(request):
    return render(request, 'tax_office/list_tax_office.html')


class TaxOfficeListJson(BaseDatatableView):
    model = TaxOffice
    columns = ['id', 'name', 'created_at']
    order_columns = ['id', 'name', 'created_at']

    def filter_queryset(self, qs):
        sSearch = self.request.GET.get('search[value]', None)
        if sSearch:
            qs = qs.filter(
                Q(name__istartswith=sSearch)
            )
        return qs

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'created_at':
            # escape HTML for security reasons
            # return escape('{0} {1}'.format(row.customer_firstname, row.customer_lastname))
            return datetime.strftime(row.created_at, "%Y-%m-%d %H:%M:%S")
        else:
            print(row)
            print(column)
            return super(TaxOfficeListJson, self).render_column(row, column)


class TaxOfficeCreateView(BSModalCreateView):
    template_name = 'tax_office/create_tax_office.html'
    form_class = TaxOfficeModelForm
    success_message = 'Başarılı: Vergi dairesi oluşturuldu.'
    success_url = reverse_lazy('tax-office-list')


class TaxOfficeUpdateView(BSModalUpdateView):
    model = TaxOffice
    template_name = 'tax_office/update_tax_office.html'
    form_class = TaxOfficeModelForm
    success_message = 'Başarılı: vergi dairesi güncellendi.'
    success_url = reverse_lazy('tax-office-list')


class TaxOfficeDeleteView(BSModalDeleteView):
    model = TaxOffice
    template_name = 'tax_office/delete_tax_office.html'
    success_message = 'Başarılı: firma silindi.'
    success_url = reverse_lazy('tax-office-list')


class TaxOfficeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return TaxOffice.objects.none()

        qs = TaxOffice.objects.filter()
        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

################ TAX OFFICE #####################
