from django.shortcuts import render
from django.views.generic import TemplateView

from products.models import Product
from django.db.models import Q
# Create your views here.

class HomepageView(TemplateView):
    template_name = "shop/home.html"
    title = "Home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all().filter(Q(stock__gt=0))
        context["title"] = "Home"
        context["products"] = products[:6]  # Show only the first 6 products for the homepage
        context["title"] = self.title
        return context

class AboutView(TemplateView):
    template_name = "shop/about.html"
    title = "About Us"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context