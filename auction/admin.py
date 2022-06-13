from django.contrib import admin
from .models import Auction, Product, Category, BidTransaction

# Register your models here.
admin.site.register(Auction)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(BidTransaction)

