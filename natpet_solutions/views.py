from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views import View

from products.utils import search_all_models


class FullTextSearch(View):
    template_name = "products/search_results.html"

    def get(self, request):
        query = request.GET.get("search", "")
        print("Searching for {}".format(query))

        if query:
            results = search_all_models(query)
            print(results)
        else:
            results = []

        data = {"Keyword": query, "results": results}
        return render(request, self.template_name, data)