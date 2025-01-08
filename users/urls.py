from django.urls import path
from . import views

urlpatterns = [
    path('profile/',views.UserProfileView.as_view(), name='account_profile'),
]