from django import forms
from .models import Client, ClientCategory

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'category', 'description', 'notes')