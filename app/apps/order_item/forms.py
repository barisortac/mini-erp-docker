from bootstrap_modal_forms.forms import BSModalModelForm

from .models import OrderItem


class OrderItemModelForm(BSModalModelForm):
    class Meta:
        model = OrderItem
        fields = [
            "order",
            "product",
            "quantity",
            "package_count",
            "list_price",
            "total_amount",
            "total_amount_with_vat",
        ]
