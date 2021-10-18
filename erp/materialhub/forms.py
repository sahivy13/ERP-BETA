from django import forms
from .models import ProductMaterial, ProductMaterialCategory

class ProductMaterialForm(forms.ModelForm):
    class Meta:
        model = ProductMaterial
        fields = ('name', 'category', 'aka', 'hazard', 'description')