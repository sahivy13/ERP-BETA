from django.urls import path
from .views import (
    ClientItemRFQListView, ClientItemRFQCreateView, ClientItemRFQUpdateView, DashboardView,
    delete_rfq, rfq_action_view,
)

app_name = "rfqhub" # needed as to Django recognize app's url

# pk - primary key (syntax recognized by Django, no need to import)
urlpatterns = [
    path('', DashboardView.as_view(), name='client-rfq-dashboard'),
    path('list/', ClientItemRFQListView.as_view(), name='client-rfq-list'),
    path('create/', ClientItemRFQCreateView.as_view(), name='client-rfq-create'),
    path('<int:pk>/update/', ClientItemRFQUpdateView.as_view(), name='client-rfq-update'),
    path('<int:pk>/delete/', delete_rfq, name='delete_rfq'),
    path('action/<int:pk>/<slug:action>/', rfq_action_view, name='rfq_action'),
]