from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from .forms import AddProductForm, UpdateProductForm, PlaceBidForm, FeedbackForm
from auction.models import Product, Auction, BidTransaction
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from django.db.models import Q


# Create your views here.


def home(request):
    itemlist = Product.objects.exclude(is_online=True).exclude(is_rejected=True)
    context = {'items':itemlist}
    return render(request, 'auction/home.html', context)


def products(request):
    # exclude_filter = ~Q(is_online=True) & ~Q(is_verified=False)
    itemsList = Product.objects.exclude(is_online=True).exclude(is_rejected=True)
    context = {'items': itemsList}
    return render(request, 'auction/products.html', context)


def addproduct(request):
    if request.user.profile.user_type == "BUYER":
        return redirect('no_permission')
    form = AddProductForm()
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid() and form.cleaned_data.get('bid_start') > timezone.now() and form.cleaned_data.get(
                'bid_expiry') > form.cleaned_data.get('bid_start'):
            instance = form.save()
            instance.user_id = request.user.id
            instance.save()
            return redirect('home')
        else:
            messages.info(request, 'Your Bid Start Time and Expiry Time is contradictory')
            redirect('add-product')

    context = {'form': form}
    return render(request, 'auction/addproductform.html', context)


def singleproduct(request, pk):
    item = Product.objects.get(id=pk)
    upd = True
    dlt = True
    if item.is_online:
        if Auction.objects.filter(product_id=pk).exists():
            upd = False
            if item.auction.bid_expiry < timezone.now():
                dlt = False
    context = {'item': item, 'upd': upd, 'dlt': dlt}
    return render(request, 'auction/single_product.html', context)


def live_auction_products(request):
    items = Auction.objects.filter(bid_expiry__gte=timezone.now())
    context = {'items': items}
    return render(request, 'auction/auction_products.html', context)


def single_auction_product(request, pk):
    winner = None
    item = Auction.objects.get(id=pk)
    if BidTransaction.objects.filter(auction_id=pk).exists():
        won = BidTransaction.objects.filter(auction_id=pk).order_by("-amount").first()
        winner = won.bidder.username
    last_price = item.min_bid_price
    if not item.maximum_bid == None:
        last_price = item.maximum_bid
    context = {'item': item, 'last_price': last_price, 'winner': winner}
    return render(request, 'auction/auction_single_product.html', context)


def update_product(request, pk):
    if request.user.profile.user_type == "BUYER":
        return redirect('no_permission')
    item = Product.objects.get(id=pk)
    form = UpdateProductForm(instance=item)
    if request.method == 'POST':
        form = UpdateProductForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.info(request, 'Product information was updated')
            return redirect(reverse('single-product', args=[item.id]))
    context = {'form': form}
    return render(request, 'auction/update_product.html', context)


def delete_product(request, pk):
    if request.user.profile.user_type == "BUYER":
        return redirect('no_permission')
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('products')

    context = {'item': item}
    return render(request, 'auction/confirm_delete.html', context)


def no_permission(request):
    return render(request, 'auction/no_permission.html')


def my_products(request):
    if not request.user.profile.user_type == "SELLER":
        return render(request, 'auction/no_permission.html')
    my_auction_items = Auction.objects.filter(product__user_id=request.user.id, bid_expiry__gte=timezone.now())
    myitem = Product.objects.filter(user_id=request.user.id, is_online=False, is_rejected=False)
    rejecteditems = Product.objects.filter(user_id=request.user.id, is_rejected=True)
    context = {'items': my_auction_items, 'pendingitems': myitem, 'rejecteditems': rejecteditems}
    return render(request, 'auction/my_products.html', context)


def auction_history(request, pk):
    history_items = BidTransaction.objects.filter(bidder_id=pk)
    context = {'history_items': history_items}
    return render(request, 'auction/my_history.html', context)


def will_won_auction(pk, amount):
    tr = BidTransaction.objects.filter(auction_id=pk, has_won=True).order_by('-amount').first()
    if tr is None:
        return True
    if amount > tr.amount:
        return True
    return False


def place_bid(request, pk):
    auctionItem = Auction.objects.get(id=pk)
    if not request.user.is_authenticated:
        return render(request, 'auction/no_permission.html')
    if request.user.profile.verified_by is None:
        messages.info(request, 'You can not participate in Auction, Your Profile is not verified')
        return redirect(reverse('auction_single_product', kwargs={'pk': auctionItem.id}))
    form = PlaceBidForm()
    if request.method == "POST":
        form = PlaceBidForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            auctionItem = Auction.objects.get(id=pk)
            amount = auctionItem.maximum_bid + form.cleaned_data.get('add_amount')
            wwon = will_won_auction(auctionItem.id, amount)
            print(wwon)
            BidTransaction.objects.create(
                bidder_id=request.user.id,
                auction=auctionItem,
                amount=amount,
                has_won=wwon
            )
            if wwon:
                auctionItem.maximum_bid = amount
                auctionItem.save()
            return redirect(reverse('auction_single_product', kwargs={'pk': auctionItem.id}))
    return render(request, 'auction/auction_single_product.html')


def feedback(request):
    form = FeedbackForm()

    if request.method == "POST":

        form = FeedbackForm(data=request.POST)

        if form.is_valid():
            type = request.user.profile.user_type
            message = form.cleaned_data['feedback_message']
            username = request.user.username
            subject = "Feedback By " + type +" "+ username
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ["shamimahammadrasel@gmail.com", "shihabahmed2312@gmail.com", "cse1705017brur@gmail.com"],
                fail_silently=False,
            )
            messages.success(request, 'Your FeedBack sent to Admin, Thanks for your support and being an active user')
            return redirect("home")
    context = {'form':form}
    return render(request, 'auction/feedback.html', context)