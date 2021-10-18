from django.shortcuts import render, reverse
from django.views import generic
from .models import ProductItem
from .forms import ProductItemForm

class ProductItemListView(generic.ListView):
    template_name = "itemhub/item_list.html"
    context_object_name = "items"

    def get_queryset(self):
        queryset = ProductItem.objects.all()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(ProductItemListView, self).get_context_data(**kwargs)
        return context

class ProductItemCreateView(generic.CreateView):
    template_name = "itemhub/item_create.html"
    form_class = ProductItemForm
    def get_success_url(self) -> str:
        return reverse("itemhub:productitem-list")

    def form_valid(self, form):
        item = form.save(commit=False)
        item.save()
        return super(ProductItemCreateView, self).form_valid(form)

class ProductItemUpdateView(generic.UpdateView):
    template_name = "itemhub/item_update.html"
    form_class = ProductItemForm
    
    def get_queryset(self):
        return ProductItem.objects.all()

    def get_success_url(self) -> str:
        return reverse("itemhub:productitem-list")


class ProductItemDeleteView(generic.DeleteView):
    template_name = "itemhub/item_delete.html"
    
    def get_queryset(self):
        return ProductItem.objects.all()
    
    def get_success_url(self) -> str:
        return reverse("itemhub:productitem-list")
