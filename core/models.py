from django.db import models

import uuid

# Create your models here.



class CreatedByChoices(models.TextChoices):
    rasel = 'rasel'
    shihab = 'shihab'
    sharmin = 'sharmin'



class BaseModel(models.Model):
    guid = models.UUIDField(default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class VarifiedByAbstractModel(models.Model):
    verified_by = models.CharField(max_length=200,choices=CreatedByChoices.choices, null=True, blank=True)
    is_varified = models.BooleanField(null=True, default=False)
    class Meta:
        abstract = True
