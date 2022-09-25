
from django.db import models
from core.models import BaseModel,VarifiedByAbstractModel


# Create your models here.
class UserTypeChoices(models.TextChoices):
    SELLER = 'SELLER'
    BUYER = 'BUYER'


class GenderTypeChoices(models.TextChoices):
    MALE = 'MALE'
    FEMALE = 'FEMALE'




class Profile(VarifiedByAbstractModel, BaseModel):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    user_type = models.CharField(max_length=200,choices=UserTypeChoices.choices)
    user_image = models.ImageField(default='default.png',upload_to='profiles')
    verfication_document = models.FileField(null=True, blank=True,upload_to='profiles')
    phone = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=200, choices=GenderTypeChoices.choices, null=True,blank=True)
    location = models.TextField(null=True)

    def __str__(self):
        return self.user.username


class Credit(BaseModel):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=0)
    expiry = models.DateTimeField()

    def __str__(self):
        return self.user.username


class CreditTransaction(BaseModel):
    credit = models.ForeignKey("accounts.Credit",on_delete=models.SET_NULL,null=True)
    amount = models.PositiveIntegerField(default=0)
    transaction_type = models.CharField(max_length=100)


