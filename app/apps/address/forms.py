# from __future__ import unicode_literals
# from dal import autocomplete
# from django import forms
# from django.utils.translation import ugettext_lazy as _t
# from django.urls import reverse
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout
# from crispy_forms.layout import Fieldset
# from crispy_forms.layout import ButtonHolder
# from crispy_forms.layout import Submit
# from crispy_forms.layout import HTML
# from core.forms import CoreModelForm
# from .models import Address, District, Township, State, City
#
#
# class AddressForm(CoreModelForm):
#
#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop("user")
#
#         super(AddressForm, self).__init__(*args, **kwargs)
#
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.form_class = 'form-horizontal'
#         self.helper.label_class = 'col-lg-2 col-md-2'
#         self.helper.field_class = 'col-lg-4 col-md-4'
#         # self.helper.form_show_errors = True
#         self.helper.form_error_title = _t('Errors:')
#
#         self.fields["district"] = forms.ModelChoiceField(
#             queryset=District.objects.all(),
#             label=_t("District"),
#             required=False,
#             widget=autocomplete.ModelSelect2(
#                 url='district-autocomplete',
#                 attrs={"data-placeholder": _t("Districts...")},
#                 forward=['township']
#             )
#         )
#
#         self.fields["city"] = forms.ModelChoiceField(
#             queryset=City.objects.all(),
#             label=_t("City"),
#             required=True,
#             widget=autocomplete.ModelSelect2(
#                 url='city-autocomplete',
#                 attrs={"data-placeholder": _t("City...")},
#             )
#         )
#
#         self.fields["township"] = forms.ModelChoiceField(
#             queryset=Township.objects.all(),
#             label=_t("Township"),
#             required=True,
#             widget=autocomplete.ModelSelect2(
#                 url='township-autocomplete',
#                 attrs={"data-placeholder": _t("Township")},
#                 forward=['city']
#             )
#         )
#         self.fields["state"] = forms.ModelChoiceField(
#             queryset=State.objects.all(),
#             label=_t("State"),
#             required=False,
#             widget=autocomplete.ModelSelect2(
#                 url='state-autocomplete',
#                 attrs={"data-placeholder": _t("State")}
#             )
#         )
#
#         # self.fields["address"] = forms.ModelChoiceField(
#         #    queryset=Address.objects.all(),
#         #    label=_t("Address"),
#         #    required=True,
#         #    widget=autocomplete.ModelSelect2(
#         #        url='address-autocomplete',
#         #        attrs={"data-placeholder": _t("Address...")},
#         #    )
#         # )
#
#         list_button = HTML(
#             "<a href='{}' class='btn btn-success btt'>{}</a>".format(reverse("address-list"), _t("Address List")))
#
#         if self.instance and self.instance.id:
#             save_button = _t("Update")
#         else:
#             save_button = _t("Save")
#
#         buttons = ButtonHolder(
#             Submit('submit', save_button),
#             list_button
#         )
#
#         self.helper.layout = Layout(
#             Fieldset(
#                 _t("Address Form"),
#                 buttons,
#                 'address_title',
#                 'address',
#                 'state',
#                 'city',
#                 'township',
#                 'district',
#                 'postal_code',
#                 'phone',
#                 'internal',
#                 'fax',
#                 'tax_no',
#                 'tax_office'
#             )
#         )
#
#     class Meta:
#         model = Address
#         exclude = ('created_at', 'created_by', 'is_deleted', 'is_active', 'deleted_at', 'deleted_by', 'data',)
