from django.views.generic import TemplateView
# Create your views here.

class HomePage(TemplateView):
    template_name = 'index.html'

# class CartPage(TemplateView):
#     template_name = 'cart.html'
