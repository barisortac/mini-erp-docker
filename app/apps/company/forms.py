from bootstrap_modal_forms.forms import BSModalModelForm
from dal import autocomplete
from django import forms

from .models import Company, TaxOffice


class CompanyModelForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(CompanyModelForm, self).__init__(*args, **kwargs)

        self.fields["tax_office"] = forms.ModelChoiceField(
            queryset=TaxOffice.objects.all(),
            label="Vergi Dairesi",
            required=False,
            widget=autocomplete.ModelSelect2(
                url='tax-office-autocomplete',
                attrs={"data-placeholder": "", "data-width": None}
            )
        )

    class Meta:
        model = Company
        fields = [
            "name",
            "code",
            "tax_office",
            "tax_number",
            "phone",
            "payment_type",
            "city",
        ]


class TaxOfficeModelForm(BSModalModelForm):
    class Meta:
        model = TaxOffice
        fields = [
            "name",
        ]
