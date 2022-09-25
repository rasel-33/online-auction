from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import Auction, Product, Category, BidTransaction

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(BidTransaction)


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    change_form_template = 'auction/admin/new_buttons.html'

    def response_change(self, request, obj):
        if '_product_make_online' in request.POST:
            product = obj.product
            product.is_online = True
            product.save()
            self.message_user(request, "Product is now online")
            return HttpResponseRedirect('.')

        return super(AuctionAdmin, self).response_change(request, obj)

