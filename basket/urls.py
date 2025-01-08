from django.urls import reverse
from django.urls import path
from . import views

urlpatterns = [
    path('', views.BasketView.as_view(), name='basket'),
]