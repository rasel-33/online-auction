from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import AddProductForm
from auction.models import Product
from django.contrib import messages

#Create your views here.

def home(request):
    return render(request,'main.html')

def products(request):
    itemsList = Product.objects.all().filter
    context = {'items':itemsList}
    return render(request,'products.html',context)

def addproduct(request):
    form = AddProductForm()
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid() and form.cleaned_data.get('bid_start') > timezone.now() and form.cleaned_data.get('bid_expiry') > form.cleaned_data.get('bid_start'):
            form.save()
            return redirect('home')
        else:
            messages.info(request, 'Your Bid Start Time and Expiry Time is contradictory')
            redirect('add-product')

    context = {'form':form}
    return render(request,'addproductform.html',context)

def singleproduct(request,pk):
    item = Product.objects.get(id=pk)
    context = {'item':item}
    return render(request,'single_product.html',context)

