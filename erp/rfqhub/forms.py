from django import forms
from .models import ClientItemRFQ

class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientItemRFQCreateForm(BaseForm, forms.ModelForm):
    date_received = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = ClientItemRFQ
        fields = ['client', 'rfq_number', 'date_received']

class ClientItemRFQEditForm(BaseForm, forms.ModelForm):

    class Meta:
        model = ClientItemRFQ
        fields = ['client', 'rfq_number', 'date_received']
        # widgets = {
        #     'date_received' : DateField(