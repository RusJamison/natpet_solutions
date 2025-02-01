from django.shortcuts import render
from django.views import View
from .forms import ProfileForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from checkout.models import Order, OrderItem


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


class UserOrdersView(LoginRequiredMixin,View):

      def get(self, request):
        orders_with_total_price = (
            Order.objects
            .annotate(
                total_price=Coalesce(
                    Sum(F("items__price") * F("items__quantity")),
                    0,
                    output_field=DecimalField()
                )
            ).filter(user=request.user).all()
        )
        return render(
            request,
            "users/user_orders.html",
            {
                "orders": orders_with_total_price,
            },
        )

class OrderDetailView(LoginRequiredMixin,DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'checkout/order_detail.html'  
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        context['order_items'] = self.object.items.all()
        
        context['total_cost'] = self.object.get_total_cost()
        
        return context
