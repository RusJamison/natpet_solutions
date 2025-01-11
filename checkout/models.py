from django.db import models
from products.models import Product
from users.models import Profile
from django.core.validators import MinValueValidator
# check out models
# Create your models here.
class Order(models.Model):
    """
    An Order placed by a customer. Can have multiple OrderItems.
    """
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    # For addresses, you could store snapshots of shipping/billing addresses at the time of order:
    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    billing_address = models.CharField(max_length=255, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.pk} - {self.customer.user.username if self.customer else 'Guest'}"

    def calculate_total_amount(self):
        """
        Calculate total by summing all OrderItems.
        """
        total = sum(item.subtotal() for item in self.order_items.all())
        self.total_amount = total
        self.save()
        return total


class OrderItem(models.Model):
    """
    An item in an order, tied to a specific product.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])

    def __str__(self):
        return f"OrderItem: {self.product.name} (x{self.quantity}) for order #{self.order.pk}"

    def subtotal(self):
        return self.price * self.quantity


class Payment(models.Model):
    """
    Tracks payments made against an order.
    """
    PAYMENT_STATUS = (
        ('initiated', 'Initiated'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='initiated')
    payment_method = models.CharField(max_length=50, default='credit_card')  # e.g. 'credit_card', 'paypal', etc.
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.pk} for Order #{self.order.pk}"


class Review(models.Model):
    """
    A simple review system for products.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1)]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.customer.user.username} for {self.product.name}"
