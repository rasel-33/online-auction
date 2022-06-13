from django.db import models
from core.models import BaseModel,VarifiedByAbstractModel

# Create your models here.

class Product(VarifiedByAbstractModel, BaseModel):
    owner = models.ForeignKey("auth.User",on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey("auction.Category",on_delete=models.SET_NULL,null=True)
    product_name = models.CharField(max_length=300)
    product_description = models.CharField(max_length=900)
    is_verified = models.BooleanField(default=False)
    verified_time = models.DateTimeField(auto_now_add=True,null=True)
    bid_start = models.DateTimeField()
    bid_expiry = models.DateTimeField()

class Category(BaseModel):
    added_by = models.ForeignKey("auth.User",on_delete=models.SET_NULL,null=True)
    category_name = models.CharField(max_length=200)
    category_description = models.CharField(max_length=900)

class Auction(BaseModel):
    created_by = models.ForeignKey("auth.User",on_delete=models.CASCADE)
    product = models.OneToOneField("auction.Product",on_delete=models.CASCADE)
    min_bid_price = models.PositiveIntegerField()
    bid_start = models.DateTimeField()
    bid_expiry = models.DateTimeField()
    min_required_credit = models.PositiveIntegerField()

class BidTransaction(BaseModel):
    bidder = models.ForeignKey("auth.User",on_delete=models.SET_NULL,null=True)
    auction = models.ForeignKey("auction.Auction",on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    has_won = models.BooleanField()
