from django.shortcuts import render, reverse, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum, Count
from django_tables2 import RequestConfig
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from .models import ClientItemRFQ, RFQItem
from .forms import ClientItemRFQCreateForm, ClientItemRFQEditForm
from .tables import ClientItemRFQTable, ProductTable, RFQItemTable
from itemhub.models import ProductItem

import datetime


# @method_decorator(staff_member_required, name='dispatch')
class DashboardView(generic.ListView):
    template_name = 'clientrfqs/dashboard.html'
    model = ClientItemRFQ
    queryset = ClientItemRFQ.objects.all()[:10]

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        rfqs = ClientItemRFQ.objects.all()

        total_rfqs_requested, total_rfqs_quoted, total_rfqs_ordered= 0, 0, 0

        # total_sales = rfqs.aggregate(Sum('final_value'))['final_value__sum'] if rfqs.exists() else 0
        
        total_rfqs_requested = rfqs.filter(is_requested=True).count() if rfqs.filter(is_requested=True).exists() else 0
        total_rfqs_quoted = rfqs.filter(is_quoted=True).count() if rfqs.filter(is_quoted=True).exists() else 0
        total_rfqs_ordered = rfqs.filter(is_ordered=True).count() if rfqs.filter(is_ordered=True).exists() else 0

        divider = rfqs.count() if rfqs.count() > 0 else 1

        # paid_value = rfqs.filter(is_paid=True).aggregate(Sum('final_value'))['final_value__sum'] if rfqs.filter(is_paid=True).exists() else 0

        total_rfqs_requested_percentage= round((total_rfqs_requested/divider)*100, 1)
        total_rfqs_quoted_percentage= round((total_rfqs_quoted/divider)*100, 1)
        total_rfqs_ordered_percentage= round((total_rfqs_ordered/divider)*100, 1)

        # total_rfqs_requested = f'{total_rfqs_requested}'
        # total_rfqs_quoted = f'{total_rfqs_quoted}'
        # total_rfqs_ordered = f'{total_rfqs_ordered}'

        rfqs = ClientItemRFQTable(rfqs)

        RequestConfig(self.request).configure(rfqs)

        context.update(locals())

        return context

# @method_decorator(staff_member_required, name='dispatch')
class ClientItemRFQListView(generic.ListView):
    template_name = "clientrfqs/rfq_list.html"
    paginate_by = 50
    # context_object_name = "client_item_rfqs"

    def get_queryset(self):
        queryset = ClientItemRFQ.objects.all()

        if self.request.GET:
            queryset = ClientItemRFQ.filter_data(self.request, queryset)

        return queryset
    
    def get_context_data(self, **kwargs):
        # context = super(ClientItemRFQListView, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        rfqs = ClientItemRFQTable(self.object_list)
        RequestConfig(self.request).configure(rfqs)
        context.update(locals())
        return context

class ClientItemRFQCreateView(generic.CreateView):
    template_name = "clientrfqs/rfq_create.html"
    form_class = ClientItemRFQCreateForm
    def get_success_url(self) -> str:
        return reverse("rfqhub:client-rfq-list")

    def form_valid(self, form):
        item = form.save(commit=False)
        item.save()
        return super(ClientItemRFQCreateView, self).form_valid(form)

class ClientItemRFQUpdateView(generic.UpdateView):
    template_name = "clientrfqs/rfq_update.html"
    form_class = ClientItemRFQEditForm
    
    def get_queryset(self):
        return ClientItemRFQ.objects.all()

    def get_success_url(self) -> str:
        return reverse("rfqhub:client-rfq-list")

class ClientItemRFQDeleteView(generic.DeleteView):
    template_name = "clientrfqs/rfq_delete.html"
    
    def get_queryset(self):
        return ClientItemRFQ.objects.all()
    
# @staff_member_required
def ajax_search_products(request, pk):
    instance = get_object_or_404(ClientItemRFQ, id=pk)
    q = request.GET.get('q', None)
    products = ProductItem.broswer.active().filter(name__startswith=q) if q else ProductItem.broswer.active()
    products = products[:12]
    products = ProductTable(products)
    RequestConfig(request).configure(products)
    data = dict()
    data['products'] = render_to_string(template_name='include/product_container.html',
                                        request=request,
                                        context={
                                            'products': products,
                                            'instance': instance
                                        })
    return JsonResponse(data)


# @staff_member_required
def ajax_calculate_results_view(request):

    rfqs = ClientItemRFQ.filter_data(request, ClientItemRFQ.objects.all())

    total_rfqs_requested, total_rfqs_quoted, total_rfqs_ordered, data = 0, 0, 0, dict()

    if rfqs.exists():

        total_rfqs_requested = rfqs.filter(is_requested=True).count() if rfqs.filter(is_requested=True).exists() else 0
        total_rfqs_quoted = rfqs.filter(is_quoted=True).count() if rfqs.filter(is_quoted=True).exists() else 0
        total_rfqs_ordered = rfqs.filter(is_ordered=True).count() if rfqs.filter(is_ordered=True).exists() else 0

    data['result'] = render_to_string(
        template_name='include/result_container.html',
        request=request,
        context=locals()
    )
    
    return JsonResponse(data)

# @staff_member_required
def ajax_calculate_category_view(request):

    rfqs = ClientItemRFQ.filter_data(request, ClientItemRFQ.objects.all())

    order_items = OrderItem.objects.filter(order__in=orders)

    category_analysis = order_items.values_list('product__category__title').annotate(
        qty=Sum('qty'),
        total_incomes=Sum('total_price')
    )

    data = dict()

    category, currency = True, CURRENCY

    data['result'] = render_to_string(
        template_name='include/result_container.html',
        request=request,
        context=locals()
    )

# Create your views here.

# @staff_member_required
def ajax_search_products(request, pk):
    instance = get_object_or_404(ClientItemRFQ, id=pk)
    q = request.GET.get('q', None)
    products = ProductItem.broswer.active().filter(title__startswith=q) if q else ProductItem.broswer.active()
    products = products[:12]
    products = ProductTable(products)
    RequestConfig(request).configure(products)
    data = dict()
    data['products'] = render_to_string(template_name='include/product_container.html',
                                        request=request,
                                        context={
                                            'products': products,
                                            'instance': instance
                                        })
    return JsonResponse(data)