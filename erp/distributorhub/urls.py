from django.urls import path
from .views import (
    DistributorListView, DistributorCreateView, DistributorUpdateView, DistributorDeleteView
)

app_name = "distributorhub" # needed as to Django recognize app's url

# pk - primary key (syntax recognized by Django, no need to import)
urlpatterns = [
    path('', DistributorListView.as_view(), name='distributor-list'),
    path('create/', DistributorCreateView.as_view(), name='distributor-create'),
    # path('<int:pk>/', LeadDetailView.as_view() , name='lead-detail'), #int: is needed to diferentiate between id number and other page inside of leads app
    path('<int:pk>/update/', DistributorUpdateView.as_view(), name='distributor-update'),
    path('<int:pk>/delete/', DistributorDeleteView.as_view(), name='distributor-delete'),
    # path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    # path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
]