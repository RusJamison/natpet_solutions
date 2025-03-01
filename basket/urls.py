from django.urls import path
from . import views

urlpatterns = [
    path("", views.BasketDetailView.as_view(), name="basket"),
    path("add/<product_id>", views.AddToBasketView.as_view(), name="basket_add"),
    path("add_product/<product_id>", views.AddToBasketProductView.as_view(), name="add_to_basket_product"),  # for adding product to basket on the product page
    path("remove/<product_id>", views.RemoveBasketProduct.as_view(), name="basket_remove"),
    path("update_quantity/<product_id>", views.UpdateItemQuantity.as_view(), name="update_item_quantity"),  # for updating quantity of items in the basket
    
]