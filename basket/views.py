from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages

from basket.basket import Basket
from basket.forms import BasketAddProductForm
from products.models import Product


# Create your views here.
class AddToBasketView(View):
    def post(self, request, product_id):
        basket = Basket(request)
        product = get_object_or_404(Product, id=product_id)
        form = BasketAddProductForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            basket.add(
                product=product,
                quantity=cd["quantity"],
                override_quantity=cd["override"],
            )
        messages.success(request,
                         f"{product.name} has been added to your basket.")
        return redirect("basket")


class AddToBasketProductView(View):
    """Add a product to basket on the product card"""

    def post(self, request, product_id):
        basket = Basket(request)
        product = get_object_or_404(Product, id=product_id)
        basket.add(product, 1, override_quantity=False)
        messages.success(request,
                         f"{product.name} has been added to your basket.")
        return redirect(request.META["HTTP_REFERER"])


class RemoveBasketProduct(View):
    def post(self, request, product_id):
        basket = Basket(request)
        product = get_object_or_404(Product, id=product_id)
        basket.remove(product.id)
        messages.success(request,
                         f"{product.name} has been removed from your basket.")
        return redirect("basket")


class BasketDetailView(View):
    template_name = "basket/basket.html"
    title = "Basket"

    def get(self, request):
        basket = Basket(request)
        return render(
            request,
            self.template_name, {"Basket": basket, "title": self.title}
        )


class UpdateItemQuantity(View):
    def post(self, request, product_id):
        basket = Basket(request)
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get("quantity"))
        override_quantity = True
        basket.add(product, quantity, override_quantity=override_quantity)
        messages.success(request,
                         f"Quantity of {product.name} has been updated.")
        return redirect("basket")
