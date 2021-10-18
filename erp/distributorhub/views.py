from django.shortcuts import render, reverse
from django.views import generic
from .models import Distributor
from .forms import DistributorForm

class DistributorListView(generic.ListView):
    template_name = "distributorhub/distributor_list.html"
    context_object_name = "distributor"

    def get_queryset(self):
        queryset = Distributor.objects.all()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(DistributorListView, self).get_context_data(**kwargs)
        return context

class DistributorCreateView(generic.CreateView):
    template_name = "distributorhub/distributor_create.html"
    form_class = DistributorForm
    def get_success_url(self) -> str:
        return reverse("distributorhub:distributor-list")

    def form_valid(self, form):
        item = form.save(commit=False)
        item.save()
        return super(DistributorCreateView, self).form_valid(form)

class DistributorUpdateView(generic.UpdateView):
    template_name = "distributorhub/distributor_update.html"
    form_class = DistributorForm
    
    def get_queryset(self):
        return Distributor.objects.all()

    def get_success_url(self) -> str:
        return reverse("distributorhub:distributor-list")


class DistributorDeleteView(generic.DeleteView):
    template_name = "distributorhub/distributor_delete.html"
    
    def get_queryset(self):
        return Distributor.objects.all()
    
    def get_success_url(self) -> str:
        return reverse("distributorhub:distributor-list")
