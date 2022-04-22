from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

# Create your views here.

class RedirectToInicioView(TemplateView):    
    def get(self, request):
        return HttpResponseRedirect('inicio/')
    

class TemplateInicioView(TemplateView):
    template_name = "seguroprivado/inicio.html"