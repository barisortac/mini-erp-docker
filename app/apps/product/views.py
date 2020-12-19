from datetime import datetime

from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views import generic


from .models import Product, ProductType
from .forms import ProductModelForm, ProductTypeModelForm


@login_required
def product_list(request):
    return render(request, 'product/list_product.html')

@login_required
def get_product(request, pk=None):
    p = Product.objects.get(id=pk)
    return JsonResponse(p._json())


class ProductListJson(BaseDatatableView):
    model = Product
    columns = ["id", "name", "description", "package_unit", "product_type", "buying_price", "selling_price", "vat_rate"]
    order_columns = ["id", "name", "description", "package_unit", "product_type", "buying_price", "selling_price", "vat_rate"]

    def filter_queryset(self, qs):
        sSearch = self.request.GET.get('search[value]', None)
        if sSearch:
            qs = qs.filter(
                Q(name__istartswith=sSearch) |
                Q(product_type__istartswith=sSearch) |
                Q(description__istartswith=sSearch)
            )
        return qs

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'created_at':
            # escape HTML for security reasons
            # return escape('{0} {1}'.format(row.customer_firstname, row.customer_lastname))
            return datetime.strftime(row.created_at, "%Y-%m-%d %H:%M:%S")
        else:
            return super(ProductListJson, self).render_column(row, column)


class Index(generic.ListView):
    model = Product
    context_object_name = 'product'
    template_name = 'index.html'


class ProductCreateView(BSModalCreateView):
    template_name = 'product/create_product.html'
    form_class = ProductModelForm
    success_message = 'Başarılı: Ürün oluşturuldu.'
    success_url = reverse_lazy('list-product')


class ProductUpdateView(BSModalUpdateView):
    model = Product
    template_name = 'product/update_product.html'
    form_class = ProductModelForm
    success_message = 'Başarılı: ürün güncellendi.'
    success_url = reverse_lazy('list-product')


class ProductReadView(BSModalReadView):
    model = Product
    template_name = 'product/read_product.html'


class ProductDeleteView(BSModalDeleteView):
    model = Product
    template_name = 'product/delete_product.html'
    success_message = 'Başarılı: firma silindi.'
    success_url = reverse_lazy('list-product')


####### PRODUCT TYPE ##########
class ProductTypeListJson(BaseDatatableView):
    model = ProductType
    columns = ["id", "name"]
    order_columns = ["id", "name"]

    def filter_queryset(self, qs):
        sSearch = self.request.GET.get('search[value]', None)
        if sSearch:
            qs = qs.filter(
                Q(name__istartswith=sSearch) |
                Q(product_type__istartswith=sSearch) |
                Q(description__istartswith=sSearch)
            )
        return qs

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'created_at':
            # escape HTML for security reasons
            # return escape('{0} {1}'.format(row.customer_firstname, row.customer_lastname))
            return datetime.strftime(row.created_at, "%Y-%m-%d %H:%M:%S")
        else:
            return super(ProductTypeListJson, self).render_column(row, column)


@login_required
def product_type_list(request):
    return render(request, 'product_type/list_product_type.html')


class ProductTypeCreateView(BSModalCreateView):
    template_name = 'product_type/create_product_type.html'
    form_class = ProductTypeModelForm
    success_message = 'Başarılı: Ürün Tipi oluşturuldu.'
    success_url = reverse_lazy('list-product-type')


class ProductTypeUpdateView(BSModalUpdateView):
    model = ProductType
    template_name = 'product_type/update_product_type.html'
    form_class = ProductTypeModelForm
    success_message = 'Başarılı: ürün güncellendi.'
    success_url = reverse_lazy('list-product-type')


class ProductTypeReadView(BSModalReadView):
    model = ProductType
    template_name = 'product_type/read_product_type.html'


class ProductTypeDeleteView(BSModalDeleteView):
    model = ProductType
    template_name = 'product_type/delete_product_type.html'
    success_message = 'Başarılı: Ürün tipi silindi.'
    success_url = reverse_lazy('list-product-type')

####### PRODUCT TYPE ##########
