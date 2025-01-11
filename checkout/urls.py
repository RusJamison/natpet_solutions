from django.urls import path
from . import views

urlpatterns = [
    path('', views.CheckoutPage.as_view(), name='checkout_page'),
]