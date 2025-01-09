from django.views.generic import ListView

from products.models import Product


class ProductListView(ListView):
    model = Product
    paginate_by = 10
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    ordering = ['-created_at']
    queryset = Product.objects.all()
