from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from natpet_solutions.utils import send_template_email
from .forms import OrderCreateForm, CouponApplyForm
from .models import Coupon, Order, OrderItem
from basket.basket import Basket
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.http import HttpResponse


class CheckoutPage(LoginRequiredMixin, View):
    template_name = "checkout/checkout.html"
    success_template_name = "checkout/checkout_success.html"

    def get(self, request):
        """Handle GET requests."""
        user_profile = self.request.user.customer_profile
        user_profile_data = {
            "first_name": user_profile.first_name,
            "last_name": user_profile.last_name,
            "address": user_profile.address,
            "postal_code": user_profile.postal_code,
            "city": user_profile.city,
        }
        basket = Basket(request)
        form = OrderCreateForm(initial=user_profile_data)
        coupon_form = CouponApplyForm()
        return render(
            request,
            self.template_name,
            {"basket": basket, "form": form, "coupon_form": coupon_form},
        )

    def post(self, request):
        """Handle POST requests."""
        basket = Basket(request)
        form = OrderCreateForm(request.POST)
        print("Order created {}".format(form.is_valid()))
        if form.is_valid():
            order = form.save(commit=False)
            order.user = self.request.user
            order.save()
            for item in basket:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            request.session["order_id"] = order.id  # Store the order ID in the session
            basket.clear()  # Clear the basket after creating the order
            return redirect(reverse("process_payment"))
        return render(request, self.template_name, {"basket": basket, "form": form})


class CouponApplyView(LoginRequiredMixin, View):
    def post(self, request):
        """Handle POST requests to apply a coupon."""
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get("code")
            try:
                coupon = Coupon.objects.get(code=code, active=True)
                if not coupon.is_valid():
                    return HttpResponse("This coupon has expired or is not valid.")
                request.session["coupon_code"] = code
                messages.success(request, "Coupon Code Applied Successfully.")
                return redirect(reverse("checkout_page"))
            except Coupon.DoesNotExist:
                return HttpResponse("Invalid coupon code.")
        return redirect(reverse("checkout_page"))


class PaymentProcessView(LoginRequiredMixin, View):
    template_name = "checkout/process.html"

    def get(self, request):
        """Handle GET requests to display the payment page."""
        order_id = request.session.get("order_id", None)
        print("order_id: ", order_id)

        coupon_code = request.session.get("coupon_code", None)

        order = get_object_or_404(Order, id=order_id)

        order_details = order.get_total_cost(coupon_code)

        print("Order Details: ", order_details)
        return render(
            request, self.template_name, {"order": order, "total": order_details}
        )

    def post(self, request):
        """Handle POST requests to process the payment."""
        # get order id and coupon code from session
        order_id = request.session.get("order_id", None)
        coupon_code = request.session.get("coupon_code", None)

        # retrieve order
        order = get_object_or_404(Order, id=order_id)

        # initialize cost information
        cost_total = 0
        total_in_cents = 0

        # use the order and coupon code to get the final price
        if not coupon_code:
            cost_total = order.get_total_cost(coupon_code)
            total_in_cents = int(cost_total * Decimal("100"))
            print("Total in cents: ", total_in_cents)
        else:

            cost_total = order.get_total_cost(coupon_code)
            total_in_cents = int(cost_total["total"] * Decimal("100"))

        # URLs for payment success and cancellation
        success_url = request.build_absolute_uri(reverse("payment_completed"))
        cancel_url = request.build_absolute_uri(reverse("payment_canceled"))

        # Stripe checkout session data
        session_data = {
            "mode": "payment",
            "success_url": success_url,
            "cancel_url": cancel_url,
            "client_reference_id": str(order.id),
            "line_items": [],  # add order items to this list
        }
        # add payment info to the Stripe checkout session
        session_data["line_items"].append(
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": total_in_cents,
                    "product_data": {
                        "name": "Order Payment",
                        "description": f"Total for Order #{order.id}",
                    },
                },
                "quantity": 1,
            }
        )
        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)

        # delete coupon information
        if (
            request.session.get("coupon_code") is not None
            and request.session.get("order_id") is not None
        ):
            del request.session["coupon_code"]
            del request.session["order_id"]

        send_template_email(
            subject="Sample Email",
            to_email=request.user.email,
            template_name="order_complete",
            context={"order": order, "user": request.user},
        )

        # redirect to Stripe payment form
        return redirect(session.url, code=303)


class PaymentCompletedView(LoginRequiredMixin, TemplateView):
    template_name = "checkout/completed.html"


class PaymentCanceledView(LoginRequiredMixin, TemplateView):
    template_name = "checkout/canceled.html"


# Using Django
@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    print("signature: {}".format(sig_header))
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    if event.type == "checkout.session.completed":
        session = event.data.object
        if session.mode == "payment" and session.payment_status == "paid":
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            # mark order as paid
            order.paid = True
            order.stripe_id = session.payment_intent
            order.save()
    return HttpResponse(status=200)
