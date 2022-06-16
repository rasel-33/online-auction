from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import AddProductForm, UpdateProductForm
from auction.models import Product, Auction
from django.contrib import messages


#Create your views here.

def home(request):
    return render(request,'main.html')

def products(request):
    itemsList = Product.objects.all().exclude(is_online=True).exclude(ended=True)
    context = {'items':itemsList}
    return render(request,'auction/products.html',context)

def addproduct(request):
    form = AddProductForm()
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid() and form.cleaned_data.get('bid_start') > timezone.now() and form.cleaned_data.get('bid_expiry') > form.cleaned_data.get('bid_start'):
            form.save()
            return redirect('home')
        else:
            messages.info(request, 'Your Bid Start Time and Expiry Time is contradictory')
            redirect('add-product')

    context = {'form':form}
    return render(request,'auction/addproductform.html',context)

def singleproduct(request,pk):
    item = Product.objects.get(id=pk)
    # print(request.user.id)
    context = {'item':item}
    return render(request,'auction/single_product.html',context)

def live_auction_products(request):
    items = Auction.objects.filter(bid_expiry__gte=timezone.now())
    context = {'items':items}
    return render(request,'auction/auction_products.html',context)

def single_auction_product(request,pk):
    item = Auction.objects.get(id=pk)
    context = {'item':item}
    return render(request,'auction/auction_single_product.html',context)


def update_product(request,pk):
    form = UpdateProductForm()
    if request.method == 'POST':
        form = UpdateProductForm(request.POST, request.FILES)
        if form.is_valid():
            item = Product.objects.get(id=pk)
            item.category = form.cleaned_data.get('category')
            item.product_name = form.cleaned_data.get('product_name')
            item.product_image = form.cleaned_data.get('product_image')
            item.product_description = form.cleaned_data.get('product_description')
            item.proposed_minimum_price = form.cleaned_data.get('proposed_minimum_price')
            item.bid_start = form.cleaned_data.get('bid_start')
            item.bid_expiry = form.cleaned_data.get('bid_expiry')
            item.save()
            messages.info(request,'Product information was updated')
            return redirect('products')


    context = {'form':form}
    return render(request,'auction/update_product.html',context)





