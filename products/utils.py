from django.contrib.postgres.search import SearchQuery, SearchVector
from products.models import Category, Manufacturer, Product


def search_all_models(query):

    vector = SearchVector('name', 'description')

    print("searching for {}".format(query))

    query = SearchQuery(query)

    results = Product.objects.annotate(search=vector).filter(search=query)

    return results