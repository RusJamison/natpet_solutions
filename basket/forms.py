from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(0, 21)]


class BasketAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)
    override = forms.BooleanField(required=False,
                                  initial=False, widget=forms.HiddenInput)
