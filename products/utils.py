from django.contrib.postgres.search import SearchQuery, SearchVector
from products.models import Category, Manufacturer, Product


def search_all_models(query):
    results = Product.objects.filter(
        name__icontains=query
    ) | Product.objects.filter(
        description__icontains=query
    )

    return results.distinct()
