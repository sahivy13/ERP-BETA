from django.shortcuts import render, reverse
from django.views import generic

class HomePageView(generic.TemplateView):
    template_name = "home/homepage.html" 
