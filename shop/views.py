from django.shortcuts import render
from django.views.generic import TemplateView

from products.models import Product
# Create your views here.

class HomepageView(TemplateView):
    template_name = "shop/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        context["title"] = "Home"
        context["products"] = products[:6]  # Show only the first 6 products for the homepage
        return context

class AboutView(TemplateView):
    template_name = "shop/about.html"
