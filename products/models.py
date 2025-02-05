from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from cloudinary.models import CloudinaryField
from django.contrib.postgres.search import SearchVectorField


class Category(models.Model):
    """
    A product can belong to one or more categories.
    """

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatically generate a slug if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    A product in the shop.
    """

    name = models.CharField(max_length=255)
    model = models.CharField(max_length=250)
    description = models.TextField()
    manufacturer = models.ForeignKey(
        "Manufacturer", on_delete=models.CASCADE, related_name="equipments"
    )
    slug = models.CharField(max_length=255, blank=True)
    # bronchure =CloudinaryField(resource_type="raw", null=True, blank=True, default=None)
    notes = models.TextField(null=True, blank=True, default=None)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)]
    )
    stock = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField(Category, related_name="products", blank=True)
    image = models.ImageField(default="default.png")
    sku = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    search_vector = SearchVectorField(null=True, blank=True)
    discount = models.DecimalField(
        null=True, blank=True, default=0.0, decimal_places=2, max_digits=11
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatically generate a slug if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def discounted_price(self):
        return self.price - (self.price * (self.discount / 100))
    
    @property
    def final_price(self):
        return self.discounted_price if self.discount else self.price


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True, default=None)
    search_vector = SearchVectorField(null=True, blank=True)

    def __str__(self):
        return self.name
