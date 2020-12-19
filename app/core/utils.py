from django import forms

# inside modals, format of datetime cant be changed,
# so we can only change the datetime we send as '%Y-%m-%d'
datetime_widget_format = forms.DateTimeInput(
    format=('%Y-%m-%d'),
    attrs={
        'type': 'date',
    }
)
