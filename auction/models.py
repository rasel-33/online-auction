from datetime import datetime
from django.db import models
from core.models import BaseModel, VarifiedByAbstractModel


# Create your models here.

class Product(VarifiedByAbstractModel, BaseModel):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True)
    category = models.ForeignKey("auction.Category", on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=300)
    product_image = models.ImageField(null=True)
    product_description = models.CharField(max_length=900)
    is_rejected = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    proposed_minimum_price = models.PositiveIntegerField(default=0)
    verified_time = models.DateTimeField(auto_now_add=True, null=True)
    bid_start = models.DateTimeField(null=True)
    bid_expiry = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.product_name)


class Category(BaseModel):
    added_by = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.category_name)


class Auction(BaseModel):
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    product = models.OneToOneField("auction.Product", on_delete=models.CASCADE)
    min_bid_price = models.PositiveIntegerField()
    bid_start = models.DateTimeField()
    bid_expiry = models.DateTimeField()
    maximum_bid = models.PositiveIntegerField(null=True)
    min_required_credit = models.PositiveIntegerField()
    ended = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product.product_name)


class BidTransaction(BaseModel):
    bidder = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    auction = models.ForeignKey("auction.Auction", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    has_won = models.BooleanField()
