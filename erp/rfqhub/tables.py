import django_tables2 as tables

from itemhub.models import ProductItem
from .models import RFQItem, ClientItemRFQ

class ClientItemRFQTable(tables.Table):
    action = tables.TemplateColumn(
        '<a href="{{ record.get_edit_url }}" class="btn btn-info"><i class="fa fa-edit"></i></a>',
        orderable=False
    )

    class Meta:
        model = ClientItemRFQ
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['client','rfq_number', 'date_received', 'is_quoted']

class ProductTable(tables.Table):
    action = tables.TemplateColumn(
        '<button class="btn btn-info add_button" data-href="{% url "ajax_add" instance.id record.id %}">Add!</button>',
        orderable=False
    )

    # qty_product_input = tables.TemplateColumn(
    #     '<input id="qty_product_input" maxlength="100" name="count" type="text"/>',
    # )

    class Meta:
        model = ProductItem
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['name', 'part_number', 'brand', 'category']

class RFQItemTable(tables.Table):
    action = tables.TemplateColumn(
        '''
            <button data-href="{% url "ajax_modify" item.id "add" %}" class="btn btn-success edit_button"><i class="fa fa-arrow-up"></i></button>
            <button data-href="{% url "ajax_modify" item.id "remove" %}" class="btn btn-warning edit_button"><i class="fa fa-arrow-down"></i></button>
            <button data-href="{% url "ajax_modify" item.id "delete" %}" class="btn btn-danger edit_button"><i class="fa fa-trash"></i></button>
        ''',
        orderable=False
    )

    # qty_rfq_input = tables.TemplateColumn(
    #     '<input id="qty_rfq_input" maxlength="100" name="count" type="text"/>',
    # )

    class Meta:
        model = RFQItem
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['product.name', 'product.part_number', 'product.brand', 'product.category', 'quantity'] 