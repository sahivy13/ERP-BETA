from django.contrib import admin
from django.urls import path, include
from home.views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='homepage'),
    path('itemhub/', include('itemhub.urls', namespace="itemhub")), # application urls.py
    path('materialhub/', include('materialhub.urls', namespace="materialhub")), # application urls.py
    path('clienthub/', include('clienthub.urls', namespace="clienthub")), # application urls.py
    path('distributorhub/', include('distributorhub.urls', namespace="distributorhub")), # application urls.py
    path('producerhub/', include('producerhub.urls', namespace="producerhub")), # application urls.py
]
