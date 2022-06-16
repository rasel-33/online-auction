from django import forms
from .models import Product

class AddProductForm(forms.ModelForm):
    
    bid_start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={ 
                                           'class':'form-control',
                                           'type': 'datetime-local'}))
    bid_expiry = forms.DateTimeField(widget=forms.DateTimeInput(attrs={ 
                                           'class':'form-control',
                                           'type': 'datetime-local'}))

    class Meta:
        model = Product
        fields = ['category', 'product_name','product_image', 'product_description', 'proposed_minimum_price', 'bid_start', 'bid_expiry']

class UpdateProductForm(forms.ModelForm):
    bid_start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={ 
                                           'class':'form-control',
                                           'type': 'datetime-local'}))
    bid_expiry = forms.DateTimeField(widget=forms.DateTimeInput(attrs={ 
                                           'class':'form-control',
                                           'type': 'datetime-local'}))
    
    class Meta:
        model = Product
        fields = ['category', 'product_name','product_image', 'product_description', 'proposed_minimum_price', 'bid_start', 'bid_expiry']
