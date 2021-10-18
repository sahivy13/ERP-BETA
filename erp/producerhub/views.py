from django.shortcuts import render, reverse
from django.views import generic
from .models import Producer
from .forms import ProducerForm

class ProducerListView(generic.ListView):
    template_name = "producerhub/producer_list.html"
    context_object_name = "producer"

    def get_queryset(self):
        queryset = Producer.objects.all()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(ProducerListView, self).get_context_data(**kwargs)
        return context

class ProducerCreateView(generic.CreateView):
    template_name = "producerhub/producer_create.html"
    form_class = ProducerForm
    def get_success_url(self) -> str:
        return reverse("producerhub:Producer-list")

    def form_valid(self, form):
        item = form.save(commit=False)
        item.save()
        return super(ProducerCreateView, self).form_valid(form)

class ProducerUpdateView(generic.UpdateView):
    template_name = "producerhub/producer_update.html"
    form_class = ProducerForm
    
    def get_queryset(self):
        return Producer.objects.all()

    def get_success_url(self) -> str:
        return reverse("producerhub:producer-list")


class ProducerDeleteView(generic.DeleteView):
    template_name = "producerhub/producer_delete.html"
    
    def get_queryset(self):
        return Producer.objects.all()
    
    def get_success_url(self) -> str:
        return reverse("producerhub:producer-list")