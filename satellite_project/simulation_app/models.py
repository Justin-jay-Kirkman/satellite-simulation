import uuid

from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import AutoSlugField

SPACECRAFT_STATUS = {
    "NOMINAL": "NOMINAL",
    "MALFUNCTIONING": "MALFUNCTIONING"
}


class Spacecraft(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')

    status = models.CharField(max_length=20, choices=SPACECRAFT_STATUS, default="NOMINAL")

    def __str__(self):
        return self.name


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    satellites = models.ManyToManyField(Spacecraft)

    class Meta:
        verbose_name_plural = 'Companies'
    def __str__(self):
        return self.name