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

from order.models import Order
from .models import OrderItem
from .forms import OrderItemModelForm


@login_required
def order_item_list(request, pk=None):
    """
    pk -> order_id
    """
    context = {}
    if pk:
        order = Order.objects.filter(id=pk).select_related("company").first()
        context['order_id'] = order.id
        context['company_name'] = order.company.name
        context['order_json'] = order.api_json()
    return render(request, 'order_item/list_order_item.html', context=context)


class OrderItemListJson(BaseDatatableView):
    model = OrderItem
    columns = [
            "id"
            "order",
            "product",
            "quantity",
            "package_count",
            "list_price",
            "total_amount",
            "total_amount_with_vat",
        ]
    order_columns = [
            "id"
            "order",
            "product",
            "quantity",
            "package_count",
            "list_price",
            "total_amount",
            "total_amount_with_vat",
        ]

    def get_initial_queryset(self):
        if not self.model:
            raise NotImplementedError("Need to provide a model or implement get_initial_queryset!")

        initial_queryset = self.model.objects

        if self.kwargs and self.kwargs.get("pk"):
            return initial_queryset.filter(order_id=self.kwargs.get("pk"))
        else:
            return self.model.objects.all()

    def filter_queryset(self, qs, pk=None):
        if pk:
            qs = qs.filter(order_id=pk)
        sSearch = self.request.GET.get('search[value]', None)
        if sSearch:
            qs = qs.filter(
                Q(company__name__istartswith=sSearch) |
                Q(order__name__istartswith=sSearch) |
                Q(quantity=sSearch)
            )
        return qs

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'created_at':
            # escape HTML for security reasons
            # return escape('{0} {1}'.format(row.customer_firstname, row.customer_lastname))
            return datetime.strftime(row.created_at, "%Y-%m-%d %H:%M:%S")
        else:
            return super(OrderItemListJson, self).render_column(row, column)


class Index(generic.ListView):
    model = OrderItem
    context_object_name = 'order_item'
    template_name = 'index.html'

    def get_queryset(self):
        print(self)
        super(Index, self).get_queryset()


def get_success_url_overwrite(self):
    """
    !!!We will redirect after success order creation to the order item!!!
    Return the URL to redirect to after processing a valid form.
    """
    if self.success_url:
        url = self.success_url.format(**self.object.__dict__)
        if self.object and self.object.id:
            url = url + str(self.object.order.id)
    else:
        try:
            url = self.object.get_absolute_url()
        except AttributeError:
            raise ImproperlyConfigured(
                "No URL to redirect to.  Either provide a url or define"
                " a get_absolute_url method on the Model.")
    return url


class OrderItemCreateView(BSModalCreateView):
    template_name = 'order_item/create_order_item.html'
    form_class = OrderItemModelForm
    success_message = 'Başarılı: Sipariş kalemi oluşturuldu.'
    success_url = reverse_lazy('list-order-item')

    def get_success_url(self):
        return get_success_url_overwrite(self=self)


class OrderItemUpdateView(BSModalUpdateView):
    model = OrderItem
    template_name = 'order_item/update_order_item.html'
    form_class = OrderItemModelForm
    success_message = 'Başarılı: Sipariş kalemi güncellendi.'
    success_url = reverse_lazy('list-order-item')

    def get_success_url(self):
        return get_success_url_overwrite(self=self)



class OrderItemDeleteView(BSModalDeleteView):
    model = OrderItem
    template_name = 'order/delete_order.html'
    success_message = 'Başarılı: Sipariş kalemi silindi.'
    success_url = reverse_lazy('list-order-item')

    def get_success_url(self):
        return get_success_url_overwrite(self=self)
