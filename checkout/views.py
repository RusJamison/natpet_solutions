from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import OrderCreateForm
from .models import Order, OrderItem
from basket.basket import Basket
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView
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
            "email" :request.user.email
        }
        basket = Basket(request)
        form = OrderCreateForm(initial=user_profile_data)
        return render(request, self.template_name, {"basket": basket, "form": form})

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


class PaymentProcessView(LoginRequiredMixin, View):
    template_name = "checkout/process.html"

    def get(self, request):
        """Handle GET requests to display the payment page."""
        order_id = request.session.get("order_id", None)
        order = get_object_or_404(Order, id=order_id)
        return render(request, self.template_name, {"order": order})

    def post(self, request):
        """Handle POST requests to process the payment."""
        order_id = request.session.get("order_id", None)
        print("Order ID: ", order_id)
        order = get_object_or_404(Order, id=order_id)

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
        # add order items to the Stripe checkout session
        for item in order.items.all():
            session_data["line_items"].append(
                {
                    "price_data": {
                        "unit_amount": int(item.price * Decimal("100")),
                        "currency": "eur",
                        "product_data": {
                            "name": item.product.name,
                        },
                    },
                    "quantity": item.quantity,
                }
            )
            # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
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
    # if event.type == "checkout.session.completed":
    #     session = event.data.object
    #     if session.mode == "payment" and session.payment_status == "paid":
    #         try:
    #             order = Order.objects.get(id=session.client_reference_id)
    #         except Order.DoesNotExist:
    #             return HttpResponse(status=404)
    #         # mark order as paid
    #         order.paid = True
    #         order.stripe_id = session.payment_intent
    #         order.save()
    # return HttpResponse(status=200)
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        order_id = payment_intent['metadata'].get('order_id')
        if order_id:
            order = Order.objects.get(id=order_id)
            order.paid = True
            order.save()

    return HttpResponse(status=200)



