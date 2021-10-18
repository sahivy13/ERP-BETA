from django import forms
from .models import ProductItem, ProductItemCategory

class ProductItemForm(forms.ModelForm):
    class Meta:
        model = ProductItem
        fields = ('name', 'category', 'part_number', 'brand', 'weight', 'volume', 'description')
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'category': forms.Select(choices=ProductItemCategory.objects.all()),
        #     'part_number': forms.TextInput(attrs={'class': 'form-control'}),
        #     'brand': forms.TextInput(attrs={'class': 'form-control'}),
        #     'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        #     'volume': forms.NumberInput(attrs={'class': 'form-control'}),
        #     'description': forms.Textarea(attrs={'class': 'form-control'}),
        # }