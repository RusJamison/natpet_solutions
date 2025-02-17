from django.shortcuts import render
from django.views import View

from checkout.models import Order
from .forms import ProfileForm
from django.contrib import messages
from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Coalesce
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class UserProfileView(View):
    form_class = ProfileForm
    title = "User Profile"

    def get(self, request):
        user = request.user
        profile = user.customer_profile
        form = self.form_class(instance=profile)
        return render(
            request, "users/user_profile.html", {"form": form, "title": self.title}
        )

    def post(self, request):
        user = request.user
        profile = user.customer_profile
        form = self.form_class(request.POST, instance=profile)
        # print("form valid: {}".format(form))
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Profile update failed")
        return render(
            request, "users/user_profile.html", {"form": form, "title": self.title}
        )


# Create your views here.
class UserOrdersView(LoginRequiredMixin, View):
    title = "User Orders"
    items_per_page = 10

    def get(self, request):
        orders_with_total_price = (
            Order.objects.annotate(
                total_price=Coalesce(
                    Sum(F("items__price") * F("items__quantity")),
                    0,
                    output_field=DecimalField(),
                )
            )
            .filter(user=request.user)
            .all()
        )

        paginator = Paginator(orders_with_total_price, self.items_per_page)

        page = request.GET.get("page", 1)

        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)

        # Pagination range logic
        page_numbers = list(paginator.page_range)
        current_page = orders.number
        pagination_range = page_numbers[max(0, current_page - 3) : current_page + 2]

        return render(
            request,
            "users/user_orders.html",
            {
                "page_obj": orders,
                "paginator": paginator,
                "pagination_range": pagination_range,
                "title": self.title,
            },
        )

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    context_object_name = "order"
    template_name = "users/order_detail.html"
    title = "Order Details"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["order_items"] = self.object.items.all()

        context["total_cost"] = self.object.get_total_cost()
        context['title']=self.title
        return context
