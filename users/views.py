from django.shortcuts import render
from django.views import View

# Create your views here.
class UserProfileView(View):
    def get(self, request):
        return render(request, 'users/user_profile.html')
