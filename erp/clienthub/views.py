from django.shortcuts import render, reverse
from django.views import generic
from .models import Client
from .forms import ClientForm

class ClientListView(generic.ListView):
    template_name = "clienthub/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        queryset = Client.objects.all()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        return context

class ClientCreateView(generic.CreateView):
    template_name = "clienthub/client_create.html"
    form_class = ClientForm
    def get_success_url(self) -> str:
        return reverse("clienthub:client-list")

    def form_valid(self, form):
        item = form.save(commit=False)
        item.save()
        return super(ClientCreateView, self).form_valid(form)

class ClientUpdateView(generic.UpdateView):
    template_name = "clienthub/client_update.html"
    form_class = ClientForm
    
    def get_queryset(self):
        return Client.objects.all()

    def get_success_url(self) -> str:
        return reverse("clienthub:client-list")


class ClientDeleteView(generic.DeleteView):
    template_name = "clienthub/client_delete.html"
    
    def get_queryset(self):
        return Client.objects.all()
    
    def get_success_url(self) -> str:
        return reverse("clienthub:client-list")
