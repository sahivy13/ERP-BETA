from django.shortcuts import render, reverse, get_object_or_404, redirect
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

# @method_decorator(staff_member_required, name='dispatch')
class ClientItemRFQCreateView(generic.CreateView):
    template_name = "clientrfqs/rfq_create.html"
    form_class = ClientItemRFQCreateForm
    model = ClientItemRFQ

    def get_success_url(self) -> str:
        self.new_object.refresh_from_db()
        return reverse("rfqhub:client-rfq-update", kwargs={'pk': self.new_object.id})

    def form_valid(self, form):
        object = form.save()
        object.refresh_from_db()
        self.new_object = object
        return super(ClientItemRFQCreateView, self).form_valid(form)

# @method_decorator(staff_member_required, name='dispatch')
class ClientItemRFQUpdateView(generic.UpdateView):
    template_name = "clientrfqs/rfq_update.html"
    form_class = ClientItemRFQEditForm
    model = ClientItemRFQ

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object
        rfq_p = ProductItem.objects.filter(active=True) #[:12] - THIS ONE WAS WITH django-tables2
        # products = ProductTable(rfq_p)
        # rfq_items = RFQItemTable(instance.rfq_items.all()) - THIS ONE WAS WITH django-tables2
        rfq_items = RFQItem.objects.filter(rfq=instance)
        # RequestConfig(self.request).configure(products)
        # RequestConfig(self.request).configure(rfq_items)
        context.update(locals())
        return context

    def get_success_url(self) -> str:
        return reverse("rfqhub:client-rfq-update", kwargs={'pk': self.object.id})


# --- Delete View Old Way ---
# class ClientItemRFQDeleteView(generic.DeleteView):
#     template_name = "clientrfqs/rfq_delete.html"
    
#     def get_queryset(self):
#         return ClientItemRFQ.objects.all()
    
#     def get_success_url(self) -> str:
#         return reverse("rfqhub:client-rfq-list")

# @staff_member_required
def delete_rfq(request, pk):
    instance = get_object_or_404(ClientItemRFQ, id=pk)
    instance.delete()
    messages.warning(request, 'The rfq is deleted!')
    return redirect(reverse('rfqhub:client-rfq-list'))

# @staff_member_required - replaces done_order_view
def quoted_rfq_view(request, pk):
    instance = get_object_or_404(ClientItemRFQ, id=pk)
    instance.is_quoted = True
    instance.save()
    messages.warning(request, 'The RFQ has been marked as quoted!')
    return redirect(reverse('rfqhub:client-rfq-list'))

# @staff_member_required
def ajax_add_product(request, pk, dk):

    instance = get_object_or_404(ClientItemRFQ, id=pk)
    product = get_object_or_404(ProductItem, id=dk)

    rfq_item, created = RFQItem.objects.get_or_create(rfq=instance, product=product)

    if created:
        rfq_item.quantity = 1
        # order_item.price = product.value
        # order_item.discount_price = product.discount_value

    else:
        rfq_item.quantity += 1

    rfq_item.save()

    instance.refresh_from_db()

    rfq_items = instance.rfq_items.all()

    data = dict()

    data['result'] = render_to_string(
        template_name='include/rfq_container_ajax.html',
        request=request,context={
            'instance': instance,
            'rfq_items': rfq_items
        }
    )

    return JsonResponse(data)

# @staff_member_required
def ajax_modify_rfq_item(request, pk, action):

    rfq_item = get_object_or_404(RFQItem, id=pk)

    instance = get_object_or_404(ClientItemRFQ, id=rfq_item.rfq_id)

    if action == 'remove':
        rfq_item.quantity -= 1

        if rfq_item.quantity < 1:
            rfq_item.quantity = 1

    if action == 'add':
        rfq_item.quantity += 1

    rfq_item.save()

    if action == 'delete':
        rfq_item.delete()

    instance.refresh_from_db()

    rfq_items = instance.rfq_items.all()

    data = dict()

    data['result'] = render_to_string(
        template_name='include/rfq_container_ajax.html',
        request=request,
        context={
            'instance': instance,
            'rfq_items': rfq_items,
        }
    )

    return JsonResponse(data)


# @staff_member_required
# def ajax_modify_rfq_item(request, pk, action):

#     rfq_item = get_object_or_404(RFQItem, id=pk)
#     # product = rfq_item.product
#     instance = rfq_item.rfq

#     if action == 'remove':
#         rfq_item.quantity -= 1
#         # product.qty += 1
#         if rfq_item.quantity < 1:
#             rfq_item.quantity = 1

#     if action == 'add':
#         rfq_item.quantity += 1
#         # product.qty -= 1

#     # product.save()
#     rfq_item.save()

#     if action == 'delete':
#         rfq_item.delete()

#     data = dict()
#     instance.refresh_from_db()

#     # rfq_items = RFQItemTable(instance.rfq_items.all())
#     rfq_items = instance.rfq_items.all()

#     RequestConfig(request).configure(rfq_items)

#     data['result'] = render_to_string(
#         template_name='include/rfq_container.html',
#         request=request,
#         context={
#             'instance': instance,
#             'rfq_items': rfq_items
#         }
#     )

#     return JsonResponse(data)

# @staff_member_required
def ajax_search_products(request, pk):
    instance = get_object_or_404(ClientItemRFQ, id=pk)
    q = request.GET.get('q', None)
    products = ProductItem.broswer.active().filter(name__startswith=q) if q else ProductItem.broswer.active()
    products = products[:12]
    products = ProductTable(products)
    RequestConfig(request).configure(products)
    data = dict()
    data['products'] = render_to_string(
        template_name='include/product_container.html',
        request=request,
        context={
            'products': products,
            'instance': instance
        }
    )
    return JsonResponse(data)

# @staff_member_required
def rfq_action_view(request, pk, action):
    instance = get_object_or_404(ClientItemRFQ, id=pk)
    if action == 'is_requested': #replaces is_paid
        instance.is_requested = True
        instance.save()
    if action == 'delete':
        instance.delete()
    return redirect(reverse('client-rfq-list'))

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

    rfq_items = RFQItem.objects.filter(order__in=rfqs)

    category_analysis = rfq_items.values_list('product__category__title').annotate(
        quantity=Sum('quantity'),
        # total_incomes=Sum('total_price')
    )

    data = dict()

    # category, currency = True, CURRENCY
    category = True

    data['result'] = render_to_string(
        template_name='include/result_container.html',
        request=request,
        context=locals()
    )

    return JsonResponse(data)
