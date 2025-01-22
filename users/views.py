from django.shortcuts import render
from django.views import View
from .forms import ProfileForm
from django.contrib import messages


# Create your views here.
class UserProfileView(View):
    form_class = ProfileForm

    def get(self, request):
        user = request.user
        profile = user.customer_profile
        form = self.form_class(instance=profile)
        return render(request, "users/user_profile.html", {"form": form})
    def post(self,request):
        user = request.user
        profile = user.customer_profile
        form = self.form_class(request.POST, instance=profile)
        #print("form valid: {}".format(form))
        if form.is_valid():
            form.save()
            messages.success(request,"Profile updated successfully")
        else:
            messages.error(request, "Profile update failed")
        return render(request, "users/user_profile.html", {"form": form})


class UserOrdersView(View):

    def get(self, request):
        return render(
            request,
            "users/user_orders.html",
        )
