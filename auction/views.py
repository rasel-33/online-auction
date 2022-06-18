from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from requests import delete
from .forms import AddProductForm, UpdateProductForm
from auction.models import Product, Auction
from django.contrib import messages

from django.db.models import Q

#Create your views here.

def home(request):
    return render(request,'main.html')

def products(request):
    # exclude_filter = ~Q(is_online=True) & ~Q(is_verified=False)
    itemsList = Product.objects.exclude(is_online=True)
    context = {'items':itemsList}
    return render(request,'auction/products.html',context)

def addproduct(request):
    if request.user.profile.user_type == "BUYER":
        return redirect('no_permission')
    form = AddProductForm()
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid() and form.cleaned_data.get('bid_start') > timezone.now() and form.cleaned_data.get('bid_expiry') > form.cleaned_data.get('bid_start'):
            instance = form.save()
            instance.user_id=request.user.id
            instance.save()
            return redirect('home')
        else:
            messages.info(request, 'Your Bid Start Time and Expiry Time is contradictory')
            redirect('add-product')

    context = {'form':form}
    return render(request,'auction/addproductform.html',context)

def singleproduct(request,pk):
    item = Product.objects.get(id=pk)
    upd = True
    dlt = True
    if item.is_online:
        if Auction.objects.filter(product_id=pk).exists():
            upd = False
            if item.auction.bid_expiry < timezone.now():
                dlt = False
    context = {'item':item,'upd':upd,'dlt':dlt}
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
    if request.user.profile.user_type == "BUYER":
        return redirect('no_permission')
    item = Product.objects.get(id=pk)
    form = UpdateProductForm(instance=item)
    if request.method == 'POST':
        form = UpdateProductForm(request.POST, request.FILES, instance=item)
        if form.is_valid():

            form.save()
            messages.info(request,'Product information was updated')
            return redirect(reverse('single-product', args=[item.id]))
    context = {'form':form}
    return render(request,'auction/update_product.html',context)

def delete_product(request,pk):
    if request.user.profile.user_type == "BUYER":
        return redirect('no_permission')
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('products')

    context = {'item':item}
    return render(request,'auction/confirm_delete.html',context)

def no_permission(request):
    return render(request,'auction/no_permission.html')

def my_products(request):
    # auctionItems = Auction.objects.get()
    context = {}
    return render(request,'auction/my_products.html',context)

