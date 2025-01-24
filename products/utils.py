from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import Q, F
from products.models import Category, Manufacturer, Product


def search_all_models(query):
    # Define the search query
    search_query = SearchQuery(query)

    # Search in Product
    products = Product.objects.annotate(
        rank=SearchRank(F("search_vector"), search_query)
    ).filter(search_vector=search_query)

    # Combine results into a single list
    results = list(products)

    # Sort results by rank (optional)
    results.sort(key=lambda x: x.rank, reverse=True)

    return results