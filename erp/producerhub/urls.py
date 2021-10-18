from django.urls import path
from .views import (
    ProducerListView, ProducerCreateView, ProducerUpdateView, ProducerDeleteView
)

app_name = "producerhub" # needed as to Django recognize app's url

# pk - primary key (syntax recognized by Django, no need to import)
urlpatterns = [
    path('', ProducerListView.as_view(), name='producer-list'),
    path('create/', ProducerCreateView.as_view(), name='producer-create'),
    # path('<int:pk>/', LeadDetailView.as_view() , name='lead-detail'), #int: is needed to diferentiate between id number and other page inside of leads app
    path('<int:pk>/update/', ProducerUpdateView.as_view(), name='producer-update'),
    path('<int:pk>/delete/', ProducerDeleteView.as_view(), name='producer-delete'),
    # path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    # path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
]