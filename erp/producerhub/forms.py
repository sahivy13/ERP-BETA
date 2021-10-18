from django import forms
from .models import Producer, ProducerCategory

class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        fields = ('name', 'category', 'description', 'notes')