from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class BasketView(View, LoginRequiredMixin):
    def get(self, request):
        return render(request, 'basket/basket.html')
