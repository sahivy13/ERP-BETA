from django.urls import path
from .views import (
    ProductItemListView, ProductItemCreateView, ProductItemUpdateView, ProductItemDeleteView
)

app_name = "itemhub" # needed as to Django recognize app's url

# pk - primary key (syntax recognized by Django, no need to import)
urlpatterns = [
    path('', ProductItemListView.as_view(), name='productitem-list'),
    path('create/', ProductItemCreateView.as_view(), name='productitem-create'),
    # path('<int:pk>/', LeadDetailView.as_view() , name='lead-detail'), #int: is needed to diferentiate between id number and other page inside of leads app
    path('<int:pk>/update/', ProductItemUpdateView.as_view(), name='productitem-update'),
    path('<int:pk>/delete/', ProductItemDeleteView.as_view(), name='productitem-delete'),
    # path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    # path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
]