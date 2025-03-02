from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('<str:slug>/', views.ProductDetailView.as_view(),
         name='product_detail'),
]