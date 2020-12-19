from .models import Product, ProductType
from bootstrap_modal_forms.forms import BSModalModelForm

class ProductModelForm(BSModalModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "product_type",
            "package_unit",
            "product_type",
            "buying_price",
            "selling_price",
            "vat_rate"
        ]


class ProductTypeModelForm(BSModalModelForm):
    class Meta:
        model = ProductType
        fields = [
            "name",
        ]
