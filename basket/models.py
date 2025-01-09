from django.db import models
from django.core.validators import MinValueValidator

from products.models import Product
from users.models import Profile
# Create your models here.

class Basket(models.Model):
    """
    A basket belongs to a customer (or a session if not logged in).
    """
    customer = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Basket - {self.pk}"

    def total_price(self):
        """
        Calculate the total price of the basket by summing each item total.
        """
        return sum(item.subtotal() for item in self.basket_items.all())

    def total_items(self):
        """
        Count total items in the basket.
        """
        return sum(item.quantity for item in self.basket_items.all())


class BasketItem(models.Model):
    """
    An item in a basket. Relates to a product and includes quantity.
    """
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basket_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    def subtotal(self):
        return self.product.price * self.quantity



