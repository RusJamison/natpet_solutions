from django.db import models
from products.models import Product
from users.models import Profile, User
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from decimal import Decimal


class Order(models.Model):
    """
    An Order placed by a customer. Can have multiple OrderItems.
    """

    stripe_id = models.CharField(max_length=250, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    discount = models.DecimalField(max_digits=11, decimal_places=2,
                                   default=0.00)
    total_amount_paid = models.DecimalField(max_digits=11, decimal_places=2,
                                            default=0.00)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self, coupon_code=None):
        """
        Calculate the total cost, applying a discount
        if a valid coupon is provided.
        """
        total = sum(item.get_cost() for item in self.items.all())
        discount = 0

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, active=True)
            except Coupon.DoesNotExist:
                return total  # Total without discount if coupon doesn't exist

            if coupon and coupon.valid_from <= now() <= coupon.valid_to:
                discount = total * (Decimal(coupon.discount_percentage) / 100)
                discounted_total = total - discount
                return {'sub_total': total, 'discount': discount,
                        'total': discounted_total}
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items",
                              on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity


class Payment(models.Model):
    """
    Tracks payments made against an order.
    """

    PAYMENT_STATUS = (
        ("initiated", "Initiated"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS, default="initiated"
    )
    payment_method = models.CharField(
        max_length=50, default="credit_card"
    )  # e.g. 'credit_card', 'paypal', etc.
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.pk} for Order #{self.order.pk}"


class Review(models.Model):
    """
    A simple review system for products.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    customer = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        default=5, validators=[MinValueValidator(1)]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review by {self.customer.user.username} for {self.product.name}"


class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Discount in %"
    )
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def is_valid(self):
        return self.active and self.valid_from <= now() <= self.valid_to

    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"


class CouponUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Coupon usage for {self.user.username} using {self.coupon.code}"

    class Meta:
        unique_together = ["user", "coupon"]
