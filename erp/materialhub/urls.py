from django.urls import path
from .views import (
    ProductMaterialListView, ProductMaterialCreateView, ProductMaterialUpdateView, ProductMaterialDeleteView
)

app_name = "materialhub" # needed as to Django recognize app's url

# pk - primary key (syntax recognized by Django, no need to import)
urlpatterns = [
    path('', ProductMaterialListView.as_view(), name='productmaterial-list'),
    path('create/', ProductMaterialCreateView.as_view(), name='productmaterial-create'),
    # path('<int:pk>/', LeadDetailView.as_view() , name='lead-detail'), #int: is needed to diferentiate between id number and other page inside of leads app
    path('<int:pk>/update/', ProductMaterialUpdateView.as_view(), name='productmaterial-update'),
    path('<int:pk>/delete/', ProductMaterialDeleteView.as_view(), name='productmaterial-delete'),
    # path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    # path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
]