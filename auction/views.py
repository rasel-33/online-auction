from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from .forms import AddProductForm, UpdateProductForm, PlaceBidForm
from auction.models import Product, Auction, BidTransaction
from django.contrib import messages

from django.db.models import Q

#Create your views here.


def home(request):
    return render(request,'main.html')


def products(request):
    # exclude_filter = ~Q(is_online=True) & ~Q(is_verified=False)
    itemsList = Product.objects.exclude(is_online=True).exclude(is_rejected=True)
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
    last_price = item.min_bid_price
    if not item.maximum_bid == None:
        last_price = item.maximum_bid
    context = {'item':item,'last_price':last_price}
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
    if not request.user.profile.user_type == "SELLER":
        return render(request, 'auction/no_permission.html')
    my_auction_items = Auction.objects.filter(product__user_id=request.user.id,bid_expiry__gte=timezone.now())
    myitem = Product.objects.filter(user_id=request.user.id,is_online=False,is_rejected=False)
    rejecteditems = Product.objects.filter(user_id=request.user.id,is_rejected=True)
    context = {'items':my_auction_items,'pendingitems':myitem,'rejecteditems':rejecteditems}
    return render(request,'auction/my_products.html',context)

def auction_history(request, pk):
    history_items = BidTransaction.objects.filter(bidder_id=pk)
    context = {'histroy_items':history_items}
    return render(request, 'auction/my_history.html', context)




def place_bid(request,pk):
    if not request.user.authenticated:
        return render(request,'auction/no_permission.html')
    form = PlaceBidForm()
    if request.method == "POST":
        form = PlaceBidForm(request.POST)
        if form.is_valid():
            auctionItem = Auction.objects.get(id=pk)
            val = True
            if BidTransaction.objects.filter(auction=pk, has_won=True).exists():
                print("rasel")
            else:
                print("exact_rasel")
            # BidTransaction.objects.create(
            #     bidder=request.user.id,
            #     auction=Auction.pk,
            #     amount= auctionItem.maximum_bid + form.cleaned_data.get('add_amount')
            # )

    return render(request,'auction/auction_single_product.html')
