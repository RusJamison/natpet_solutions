from django.utils import timezone
from django import forms
from checkout.models import Coupon, Order
from products.models import Manufacturer, Product, Category  # Adjust import based on your app structure
from django.core.validators import MinValueValidator
from django.utils.text import slugify

class ProductForm(forms.ModelForm):
    """
    A form for creating and updating Product instances.
    """
    class Meta:
        model = Product
        fields = [
            'name', 'model', 'description', 'manufacturer', 'notes', 
            'price', 'stock', 'categories', 'image', 'sku', 'discount'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter model'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter description'}),
            'manufacturer': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes (optional)'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.00'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter SKU'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.00', 'placeholder': 'Discount (optional)'}),
        }
        labels = {
            'name': 'Product Name',
            'model': 'Model',
            'description': 'Description',
            'manufacturer': 'Manufacturer',
            'notes': 'Notes',
            'price': 'Price (€)',
            'stock': 'Stock Quantity',
            'categories': 'Categories',
            'image': 'Product Image',
            'sku': 'SKU',
            'discount': 'Discount (%)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make optional fields explicitly nullable in the form
        self.fields['notes'].required = False
        self.fields['discount'].required = False
        self.fields['categories'].required = False  # ManyToMany can be optional
        # Ensure image is optional if editing an existing product
        self.fields['image'].required = False

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock < 0:
            raise forms.ValidationError("Stock cannot be negative.")
        return stock

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        if discount is not None and discount < 0:
            raise forms.ValidationError("Discount cannot be negative.")
        return discount

class CategoryForm(forms.ModelForm):
    """
    Form for creating and editing Category instances
    """
    
    class Meta:
        model = Category
        fields = ['name']  # Excluding search_vector as it's typically managed automatically
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
        }
    
    def clean_name(self):
        """
        Validate the name field
        """
        name = self.cleaned_data['name']
        if not name.strip():
            raise forms.ValidationError("Category name cannot be empty")
        return name

class ManufacturerForm(forms.ModelForm):
    """
    Form for creating and editing Category instances
    """
    
    class Meta:
        model = Manufacturer
        fields = ['name', 'description']  # Excluding search_vector as it's typically managed automatically
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter manufacturer name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description'
            }),
        }
    
    def clean_name(self):
        """
        Validate the name field
        """
        name = self.cleaned_data['name']
        if not name.strip():
            raise forms.ValidationError("Manufacturer name cannot be empty")
        return name
    
    
class OrderForm(forms.ModelForm):
    """
    A form for creating or updating an Order.
    """
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'address',
            'postal_code',
            'city',
            'discount',
        ]  # Fields to include in the form
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Discount'}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'address': 'Street Address',
            'postal_code': 'Postal Code',
            'city': 'City',
            'discount': 'Discount Amount',
        }

    def clean_discount(self):
        """Ensure discount is not negative."""
        discount = self.cleaned_data['discount']
        if discount < 0:
            raise forms.ValidationError("Discount cannot be negative.")
        return discount

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionally make some fields required if they aren't already
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['address'].required = True
        self.fields['postal_code'].required = True
        self.fields['city'].required = True

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_percentage', 'valid_from', 'valid_to', 'active']
        widgets = {
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'valid_to': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        valid_from = cleaned_data.get('valid_from')
        valid_to = cleaned_data.get('valid_to')
        
        # Check if valid_to is not before valid_from
        if valid_from and valid_to and valid_to < valid_from:
            raise forms.ValidationError(
                "Valid to date must be after valid from date"
            )
        
        # Optional: Check if valid_from is not in the past
        if valid_from and valid_from < timezone.now():
            raise forms.ValidationError(
                "Valid from date cannot be in the past"
            )
            
        return cleaned_data
    
    def clean_discount_percentage(self):
        discount = self.cleaned_data['discount_percentage']
        if discount < 0 or discount > 100:
            raise forms.ValidationError(
                "Discount percentage must be between 0 and 100"
            )
        return discount
    
    def clean_code(self):
        code = self.cleaned_data['code'].upper()  # Optional: convert to uppercase
        return code
