from decimal import Decimal
from django.conf import settings
from basket.models import Basket
from django.http.request import HttpRequest
from django.utils.timezone import now
from checkout.models import Coupon
from products.models import Product


class Basket:
    def __init__(self, request: HttpRequest):
        self.request = request
        self.session = request.session

        # get the basket from session or create a new one if it doesn't exist
        basket = self.session.get(settings.BASKET_SESSION_ID)

        # save an empty basket in the session
        if not basket:
            basket = self.session[settings.BASKET_SESSION_ID] = {}

        self.basket = basket

    def add(self, product, quantity, override_quantity=False):
        """Add a new item to the basket"""
        product_id = str(product.id)

        if product_id not in self.basket:
            self.basket[product_id] = {'quantity': 0,
                                       'price': str(product.final_price)}

        if override_quantity:
            self.basket[product_id]['quantity'] = quantity
        else:
            self.basket[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """mark session as modified to make sure it is saved"""
        self.session.modified = True

    def remove(self, product_id):
        """Remove an item from the basket"""
        product_id = str(product_id)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def __iter__(self):
        """Iterate over the basket and get items from the database"""
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)

        basket = self.basket.copy()

        for product in products:
            self.basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """count all items in basket"""
        return sum(item['quantity'] for item in self.basket.values())

    def get_total_price(self):
        """Calculate total price of all items in basket"""
        total = (sum(Decimal(item['price']) *
                 item['quantity'] for item in self.basket.values()))

        # Apply discount if a valid coupon exists
        coupon_code = self.session.get("coupon_code")
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, active=True)
                if coupon.valid_from <= now().date() <= coupon.valid_to:
                    discount = total * (coupon.discount_percentage / 100)
                    total -= discount
            except Coupon.DoesNotExist:
                return total
        return total

    def clear(self):
        """clear the basket"""
        del self.session[settings.BASKET_SESSION_ID]
        self.save()
