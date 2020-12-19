import datetime

from django import forms
from tempus_dominus.widgets import DatePicker

from core.utils import datetime_widget_format
from .models import Order
from bootstrap_modal_forms.forms import BSModalModelForm

class DateInput(forms.DateInput):
    input_type = 'date'


class OrderModelCreateForm(BSModalModelForm):
    class Meta:
        model = Order
        fields = [
            "order_date",
            "company",
            "delivery_date",
            "order_type",
            "note",
            # "total_quantity",
            # "total_package_count",
            # "total_amount",
            # "total_amount_with_vat",
            # "discount",
            # "additional_discount",
        ]

class OrderModelUpdateForm(BSModalModelForm):
    class Meta:
        model = Order
        fields = [
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

        widgets = {
            'order_date' : datetime_widget_format,
            'delivery_date' : datetime_widget_format,
        }
