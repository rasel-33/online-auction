from django import forms
from auction.models import Product

class AddProductForm(forms.ModelForm):
    bid_start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={ 
                                           'class':'form-control',
                                           'type': 'datetime-local'}))
    bid_expiry = forms.DateTimeField(widget=forms.DateTimeInput(attrs={ 
                                           'class':'form-control',
                                           'type': 'datetime-local'}))

    class Meta:
        model = Product
        fields = ['owner', 'category', 'product_name', 'product_description', 'bid_start', 'bid_expiry']
