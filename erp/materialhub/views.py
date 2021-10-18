from django.shortcuts import render, reverse
from django.views import generic
from .models import ProductMaterial
from .forms import ProductMaterialForm

class ProductMaterialListView(generic.ListView):
    template_name = "materialhub/material_list.html"
    context_object_name = "materials"

    def get_queryset(self):
        queryset = ProductMaterial.objects.all()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(ProductMaterialListView, self).get_context_data(**kwargs)
        return context

class ProductMaterialCreateView(generic.CreateView):
    template_name = "materialhub/material_create.html"
    form_class = ProductMaterialForm
    def get_success_url(self) -> str:
        return reverse("materialhub:productmaterial-list")

    def form_valid(self, form):
        item = form.save(commit=False)
        item.save()
        return super(ProductMaterialCreateView, self).form_valid(form)

class ProductMaterialUpdateView(generic.UpdateView):
    template_name = "materialhub/material_update.html"
    form_class = ProductMaterialForm
    
    def get_queryset(self):
        return ProductMaterial.objects.all()

    def get_success_url(self) -> str:
        return reverse("materialhub:productmaterial-list")


class ProductMaterialDeleteView(generic.DeleteView):
    template_name = "materialhub/material_delete.html"
    
    def get_queryset(self):
        return ProductMaterial.objects.all()
    
    def get_success_url(self) -> str:
        return reverse("materialhub:productmaterial-list")