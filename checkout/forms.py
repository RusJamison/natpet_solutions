from django import forms
from .models import Order, Coupon


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["first_name", "last_name", "address", "postal_code", "city"]


class CouponApplyForm(forms.Form):
    code = forms.CharField(label="Coupon Code", max_length=20)

    def clean_code(self):
        code = self.cleaned_data.get("code")
        try:
            coupon = Coupon.objects.get(code=code, active=True)
            if not coupon.is_valid():
                raise forms.ValidationError("Coupon expired or not valid.")
        except Coupon.DoesNotExist:
            raise forms.ValidationError("Invalid coupon code.")
        return code