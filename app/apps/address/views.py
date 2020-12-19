# import traceback
# import sys
from dal import autocomplete
from .models import *
# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponseRedirect, JsonResponse
# from django.utils.translation import ugettext_lazy as _t
# from django.views.decorators.csrf import csrf_exempt
# from django.db import transaction
# from django.contrib import messages
# from django.urls import reverse
# from django.contrib.auth.decorators import login_required
# from address.models import Address, Township, District, City, State
# from address.forms import AddressForm
#
#
# @login_required
# def address_list(request):
#     context = {
#         'title': _t('Address List'),
#         'legend': _t('Address List')
#     }
#     return render(request, 'address_list.html', context)
#
#
# @login_required
# @csrf_exempt
# def address_list_json(request):
#     post = request.POST
#     query = post.get("search[value]")
#     start = abs(int(post.get("start", 0)))
#     size = abs(int(post.get("length", 10)))
#     draw = abs(int(post.get("draw", 1)))
#
#     columns = [
#         'address_title',
#         'address',
#         'state',
#         'city',
#         'township',
#         'district',
#         'postal_code',
#         'phone',
#         'internal',
#         'fax',
#         'first_name',
#         'last_name',
#         'tax_no',
#         'tax_office',
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
#     address = Address.objects.filter().order_by("-id")
#
#     if query:
#         address = address.filter(version__icontains=query)
#
#     if order_by:
#         address = address.order_by(order_by)
#
#     total_count = address.count()
#
#     address = address[start:end]
#
#     datas = []
#     if address:
#         for c in address:
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
# def address_form(request, pk=None):
#     post = request.POST
#
#     if pk:
#         obj = get_object_or_404(Address, pk=pk)
#     else:
#         obj = Address()
#
#     if post:
#         form = AddressForm(
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
#                             request, _t("{} Address created").format(
#                                 obj.address_title
#                             )
#                         )
#                     else:
#                         messages.success(
#                             request, _t("{} Address updated").format(
#                                 obj.address_title
#                             )
#                         )
#                     return HttpResponseRedirect(
#                         reverse("address-list"))
#
#             except Exception as e:
#                 body = '\n'.join(traceback.format_exception(*(sys.exc_info())))
#                 messages.error(request, str(e))
#
#     else:
#         form = AddressForm(
#             instance=obj, prefix="main",
#             user=request.user
#         )
#
#     context = {
#         "form": form,
#         "title": _t("Address Form"),
#     }
#
#     return render(request, "form.html", context)
#
#
# class TownshipAutocomplete(autocomplete.Select2QuerySetSequenceView):
#     def get_queryset(self):
#         use_in = self.forwarded.get('use_in', None)
#         city = self.forwarded.get('city', None)
#
#         if not self.request.user.is_authenticated:
#             return Township.objects.none()
#
#         qs = Township.objects.filter(is_active=True)
#
#         if use_in:
#             qs = qs.filter(city__use_in=use_in)
#
#         if city:
#             qs = qs.filter(city=city)
#
#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)
#
#         return qs
#
#
# class TownshipFilterAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         use_in = self.forwarded.get('use_in', None)
#         city = self.forwarded.get('city', None)
#
#         if not self.request.user.is_authenticated:
#             return Township.objects.none()
#
#         qs = Township.objects.filter(is_active=True)
#
#         if use_in:
#             qs = qs.filter(city__use_in=use_in)
#
#         if city:
#             qs = qs.filter(city=city)
#
#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)
#
#         return qs
#
#
# class DistrictAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             return District.objects.none()
#
#         qs = District.objects.all()
#
#         township = self.forwarded.get('township', None)
#
#         if township:
#             qs = qs.filter(township=township)
#
#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)
#
#         return qs
#
#
# class CityAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             return City.objects.none()
#
#         qs = City.objects.filter(is_active=True)
#
#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)
#
#         return qs
#
#
# class StateAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             return State.objects.none()
#
#         qs = State.objects.filter(is_active=True)
#
#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)
#
#         return qs
#
#
# class AddressAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             return Address.objects.none()
#
#         qs = Address.objects.filter()
#         customer = self.forwarded.get('customer', None)
#         #if customer:
#         #    qs = qs.filter(customer=customer)
#
#         if self.q:
#             qs = qs.filter(address_title__istartswith=self.q)
#
#         return qs


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return City.objects.none()

        qs = City.objects.filter(is_active=True)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs