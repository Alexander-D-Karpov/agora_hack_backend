from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.db import models

from common.file import file_path_mixing
from constructor.validators import ParentValidator


class Site(models.Model):
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, related_name="sites", on_delete=models.CASCADE)


class Block(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators = [ParentValidator]

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="content_%(class)s",
        related_query_name="children",
    )
    site = models.ForeignKey(
        Site,
        related_name="content_%(class)s",
        related_query_name="blocks",
        on_delete=models.CASCADE,
    )

    # margin
    margin_right = models.CharField(max_length=20)
    margin_left = models.CharField(max_length=20)
    margin_bottom = models.CharField(max_length=20)
    margin_top = models.CharField(max_length=20)

    # padding
    padding_right = models.CharField(max_length=20)
    padding_left = models.CharField(max_length=20)
    padding_bottom = models.CharField(max_length=20)
    padding_top = models.CharField(max_length=20)

    # size
    width = models.CharField(max_length=20)
    height = models.CharField(max_length=20)

    # color
    background_color = ColorField(default="#232325")
    color = ColorField(default="#6385b5")

    class Meta:
        abstract = True


class BaseMediaModel(models.Model):
    file = models.FileField(upload_to=file_path_mixing)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True
