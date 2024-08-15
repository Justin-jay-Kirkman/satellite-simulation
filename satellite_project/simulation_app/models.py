import uuid

from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import AutoSlugField


class Spacecraft(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')

    STATUS_CHOICES = {
        "NOMINAL": "NOMINAL",
        "MALFUNCTIONING": "MALFUNCTIONING"
    }
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NOMINAL")

    def __str__(self):
        return self.name


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    Satellites = models.ManyToManyField(Spacecraft)

    class Meta:
        verbose_name_plural = 'Companies'
    def __str__(self):
        return self.name