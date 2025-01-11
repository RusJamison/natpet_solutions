
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class CheckoutPage(View, LoginRequiredMixin):
    def get(self, request):
        return render(request, 'checkout/checkout.html')