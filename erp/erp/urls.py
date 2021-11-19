from django.contrib import admin
from django.urls import path, include
from home.views import HomePageView
from rfqhub.views import (
    ajax_search_products, ajax_add_product, ajax_modify_rfq_item, ajax_calculate_results_view, ajax_calculate_category_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='homepage'),
    path('itemhub/', include('itemhub.urls', namespace="itemhub")), # application urls.py
    path('materialhub/', include('materialhub.urls', namespace="materialhub")), # application urls.py
    path('clienthub/', include('clienthub.urls', namespace="clienthub")), # application urls.py
    path('distributorhub/', include('distributorhub.urls', namespace="distributorhub")), # application urls.py
    path('producerhub/', include('producerhub.urls', namespace="producerhub")), # application urls.py
    path('rfqhub/', include('rfqhub.urls', namespace="rfqhub")), # application urls.py

    # ajax_calls - RFQHUB
    path('ajax/search-products/<int:pk>/', ajax_search_products, name='ajax-search'),
    path('ajax/add-product/<int:pk>/<int:dk>/', ajax_add_product, name='ajax_add'),
    path('ajax/modify-product/<int:pk>/<slug:action>/', ajax_modify_rfq_item, name='ajax_modify'), #dk added to try to make it work
    path('ajax/calculate-results/', ajax_calculate_results_view, name='ajax_calculate_result'),
    path('ajax/calculate-category-results/', ajax_calculate_category_view, name='ajax_category_result'),
]
