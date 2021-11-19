from django.db import models
from django.urls import reverse
from .managers import RFQManager
from datetime import datetime
from clienthub.models import Client
from itemhub.models import ProductItem

class ClientItemRFQ(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # agent = models.ForeignKey(Agent, on_delete=models.SET_NULL)

    rfq_number = models.CharField(max_length=100)
    date_entered = models.DateField(auto_now_add=True)
    date_received = models.DateField(default=datetime.now())

    objects = models.Manager()
    browser = RFQManager()

    notes = models.TextField(null=True, blank=True)

    is_requested = models.BooleanField(default=False)
    is_quoted = models.BooleanField(default=False)
    is_ordered = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_received']
    
    def save(self, *args, **kwargs):
        rfq_items = self.rfq_items.all()
        # self.value = order_items.aggregate(Sum('total_price'))['total_price__sum'] if order_items.exists() else 0.00
        # self.final_value = Decimal(self.value) - Decimal(self.discount)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.rfq_number
    
    def get_edit_url(self):
        return reverse('rfqhub:client-rfq-update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('rfqhub:delete_rfq', kwargs={'pk': self.id})

    @staticmethod
    def filter_data(request, queryset):
        search_rfq_number = request.GET.get('search_rfq_number', None)
        date_start = request.GET.get('date_start', None)
        date_end = request.GET.get('date_end', None)
        queryset = queryset.filter(rfq_number__contains=search_rfq_number) if search_rfq_number else queryset
        if date_end and date_start and date_end >= date_start:
            date_start = datetime.strptime(date_start, '%m/%d/%Y').strftime('%Y-%m-%d')
            date_end = datetime.strptime(date_end, '%m/%d/%Y').strftime('%Y-%m-%d')
            print(date_start, date_end)
            queryset = queryset.filter(date_received__range=[date_start, date_end])
        return queryset

class RFQItem(models.Model):
    product = models.ForeignKey(ProductItem, on_delete=models.PROTECT)
    rfq = models.ForeignKey(ClientItemRFQ, on_delete=models.CASCADE, related_name='rfq_items')
    quantity = models.PositiveIntegerField(default=1)
    
    #--- THIS GOES IN THE QUOTE PRODUCT MODEL ---
    # cost = models.DecimalField(default=0.00, decimal_places=2, max_digits=11)
    # price = models.DecimalField(default=0.00, decimal_places=2, max_digits=11)

    def __str__(self):
        return f'{self.product.part_number} - {self.product.name}'

# @receiver(post_delete, sender=OrderItem)
# def delete_order_item(sender, instance, **kwargs):
#     product = instance.product
#     product.qty += instance.qty
#     product.save()
#     instance.order.save()