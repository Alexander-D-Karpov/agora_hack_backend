from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.db import models
from polymorphic.models import PolymorphicModel

from common.file import file_path_mixing
from constructor.signals import create_block, check_block
from constructor.validators import ParentValidator, MarginPaddingValidator


class Site(models.Model):
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, related_name="sites", on_delete=models.CASCADE)


class Block(PolymorphicModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators = [ParentValidator, MarginPaddingValidator]

    type = "NoType"
    is_parent = False

    parent = models.ForeignKey(
        to="self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )
    site = models.ForeignKey(
        Site,
        related_name="content_%(class)s",
        related_query_name="blocks",
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(max_length=10, blank=False, unique=True)

    # margin
    margin_right = models.CharField(max_length=20, default="none")
    margin_left = models.CharField(max_length=20, default="none")
    margin_bottom = models.CharField(max_length=20, default="none")
    margin_top = models.CharField(max_length=20, default="none")

    # padding
    padding_right = models.CharField(max_length=20, default="none")
    padding_left = models.CharField(max_length=20, default="none")
    padding_bottom = models.CharField(max_length=20, default="none")
    padding_top = models.CharField(max_length=20, default="none")

    # size
    width = models.CharField(max_length=20, default=100)
    height = models.CharField(max_length=20, default=100)

    # color
    background_color = ColorField(default="#232325")
    color = ColorField(default="#6385b5")

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        models.signals.pre_save.connect(check_block, sender=cls)
        models.signals.post_save.connect(create_block, sender=cls)

    def _get_base_json(self):
        return {
            "type": self.type,
            "margin_right": self.margin_right,
            "margin_left": self.margin_left,
            "margin_bottom": self.margin_bottom,
            "margin_top": self.margin_top,
            "padding_right": self.padding_right,
            "padding_left": self.padding_left,
            "padding_bottom": self.padding_bottom,
            "padding_top": self.padding_top,
            "width": self.width,
            "height": self.height,
            "background_color": self.background_color,
            "color": self.color,
        }

    def get_json(self):
        raise NotImplementedError


class BaseMediaModel(models.Model):
    file = models.FileField(upload_to=file_path_mixing)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True
