from datetime import datetime

from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views import generic


from .models import Order
from .forms import OrderModelCreateForm, OrderModelUpdateForm


@login_required
def order_list(request):
    return render(request, 'order/list_order.html')


class OrderListJson(BaseDatatableView):
    model = Order
    columns = [
            "id"
            "order_date",
            "company",
            "delivery_date",
            "order_type",
            "payment_type",
            "note",
            "total_quantity",
            "total_package_count",
            "discount",
            "additional_discount",
            "total_amount",
            "total_amount_with_vat",
        ]
    order_columns = [
            "id"
            "order_date",
            "company",
            "delivery_date",
            "order_type",
            "payment_type",
            "note",
            "total_quantity",
            "total_package_count",
            "discount",
            "additional_discount",
            "total_amount",
            "total_amount_with_vat",
        ]

    def filter_queryset(self, qs):
        sSearch = self.request.GET.get('search[value]', None)
        if sSearch:
            qs = qs.filter(
                Q(company__name__istartswith=sSearch) |
                Q(company__name__istartswith=sSearch)
            )
        qs = qs.order_by("-created_at")
        return qs

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'created_at':
            # escape HTML for security reasons
            # return escape('{0} {1}'.format(row.customer_firstname, row.customer_lastname))
            return datetime.strftime(row.created_at, "%d.%m.%Y")
        elif row.order_date and column == 'order_date':
            return datetime.strftime(row.order_date, "%d.%m.%Y")
        elif row.order_date and column == 'delivery_date':
            return datetime.strftime(row.delivery_date, "%d.%m.%Y")
        else:
            return super(OrderListJson, self).render_column(row, column)


class Index(generic.ListView):
    model = Order
    context_object_name = 'order'
    template_name = 'index.html'


class OrderCreateView(BSModalCreateView):
    template_name = 'order/create_order.html'
    form_class = OrderModelCreateForm
    success_message = 'Başarılı: Sipariş oluşturuldu.'
    success_url = reverse_lazy('list-order-item')

    def get_success_url(self):
        """
        !!!We will redirect after success order creation to the order item!!!
        Return the URL to redirect to after processing a valid form.
        """
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
            if self.object and self.object.id:
                url = url + str(self.object.id)
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url


class OrderUpdateView(BSModalUpdateView):
    model = Order
    template_name = 'order/update_order.html'
    form_class = OrderModelUpdateForm
    success_message = 'Başarılı: Sipariş güncellendi.'
    success_url = reverse_lazy('list-order-item')

    def get_success_url(self):
        """
        !!!We will redirect after success order creation to the order item!!!
        Return the URL to redirect to after processing a valid form.
        """
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
            if self.object and self.object.id:
                url = url + str(self.object.id)
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url


class OrderDeleteView(BSModalDeleteView):
    model = Order
    template_name = 'order/delete_order.html'
    success_message = 'Başarılı: firma silindi.'
    success_url = reverse_lazy('list-order')
