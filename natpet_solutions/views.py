from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import Category
from products.utils import search_all_models


class FullTextSearch(View, LoginRequiredMixin):
    template_name = "products/search_results.html"
    title = "Search Results"

    def get(self, request):
        query = request.GET.get("search", "")
        print("Searching for {}".format(query))
        categories = Category.objects.all()

        if query:
            results = search_all_models(query)
        else:
            results = []

        data = {"Keyword": query, "results": results, 'categories': categories, 'title': self.title}
        return render(request, self.template_name, data)
    
class RobotsViews(TemplateView):
    template_name = "robots.txt"
    content_type ="text/plain"

class SiteMapView(TemplateView):
    template_name = "sitemap.xml"
    content_type ="application/xml"