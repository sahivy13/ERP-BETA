from django import forms
from .models import Distributor, DistributorCategory

class DistributorForm(forms.ModelForm):
    class Meta:
        model = Distributor
        fields = ('name', 'category', 'description', 'notes')