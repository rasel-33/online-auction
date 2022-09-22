from django.contrib import admin
from .models import Profile, Credit, CreditTransaction

# Register your models here.
admin.site.register(Profile)
admin.site.register(Credit)
admin.site.register(CreditTransaction)