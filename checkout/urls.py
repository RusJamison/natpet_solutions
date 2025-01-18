from django.urls import path
from . import views

urlpatterns = [
    path('', views.CheckoutPage.as_view(), name='checkout_page'),
    path('payment/process/', views.PaymentProcessView.as_view(), name='process_payment'),
    path('payment/completed/', views.PaymentCompletedView.as_view(), name='payment_completed'),
    path('payment/canceled/', views.PaymentCanceledView.as_view(), name='payment_canceled'),
    path('webhook/', views.my_webhook_view, name='webhook'),

]