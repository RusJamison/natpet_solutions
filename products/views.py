from django.views.generic import ListView
from basket.forms import BasketAddProductForm
from products.models import Category, Product
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Product


class ProductListView(ListView):
    model = Product
    paginate_by = 6
    template_name = "products/product_list.html"
    context_object_name = "products"
    ordering = ["-created_at"]
    queryset = Product.objects.all()
    title = "Products"

    def get_context_data(self, **kwargs):
        # filter out products using the category
        context = super().get_context_data(**kwargs)
        category_id = self.request.GET.get("category_id", None)

        if category_id:
            context["category"] = get_object_or_404(Category, id=category_id)
            context["products"] = self.queryset.filter(
                Q(categories__name=context["category"].name)
            )

        # filter out products using the prices
        price_from = self.request.GET.get("from_price")
        price_to = self.request.GET.get("to_price")

        if price_from and price_to and price_from.isdigit() and price_to.isdigit():
            context["products"] = self.queryset.filter(
                price__range=(int(price_from), int(price_to))
            )

        # Add a list of categories to the context
        categories = Category.objects.all()
        context["categories"] = categories
        paginator = context["paginator"]  # The paginator instance
        page = context["page_obj"]  # The current page object
        context["is_paginated"] = context["is_paginated"]
        context["paginator"] = paginator
        context["page_obj"] = page

        # Additional logic for custom pagination controls
        page_numbers = list(paginator.page_range)
        current_page = page.number
        context["pagination_range"] = page_numbers[
            max(0, current_page - 3) : current_page + 2
        ]
        context['title'] = self.title
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    title = "Product Detail"

    def get_object(self, queryset=None):
        """
        fetch the product by slug.
        """
        return get_object_or_404(Product, slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        """
        Add additional context for the template if needed.
        """
        context = super().get_context_data(**kwargs)
        # Example: Add related products or reviews
        context["related_products"] = Product.objects.filter(
            categories__in=self.object.categories.all()
        ).exclude(id=self.object.id)[:4]
        context["form"] = BasketAddProductForm()
        context['title'] = self.get_object().name
        return context
