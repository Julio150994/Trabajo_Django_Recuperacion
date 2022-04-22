from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class TemplateInicioView(TemplateView):
    template_name = "seguroprivado/inicio.html"