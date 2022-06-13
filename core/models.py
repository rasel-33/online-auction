from django.db import models
import uuid

# Create your models here.


class BaseModel(models.Model):
    guid = models.UUIDField(default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class VarifiedByAbstractModel(models.Model):
    varified_by = models.ForeignKey("auth.User",on_delete=models.SET_NULL,null=True,blank=True,related_name="+")

    class Meta:
        abstract = True
