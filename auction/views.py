from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from requests import delete
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
    upd = False
    dlt = False
    if not item.is_online or item.auction.bid_expiry > timezone.now():
        upd = True
    if Auction.objects.filter(id=pk).exists():
        auction_item = Auction.objects.get(id=pk)
        if auction_item.bid_expiry > timezone.now():
            dlt = True
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
    item = Product.objects.get(id=pk)
    form = UpdateProductForm(instance=item)
    if request.method == 'POST':
        form = UpdateProductForm(request.POST, request.FILES, instance=item)
        if form.is_valid():

            form.save()
            messages.info(request,'Product information was updated')
            # return reverse_lazy('product_update', args=item.id)
            return redirect(reverse('single-product', args=[item.id]))


    context = {'form':form}
    return render(request,'auction/update_product.html',context)

