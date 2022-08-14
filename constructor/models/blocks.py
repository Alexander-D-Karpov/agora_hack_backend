from django.core.validators import MinValueValidator, MaxValueValidator

from constructor.models import Block, BaseMediaModel
from django.db import models


class FontFamily(BaseMediaModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


def get_default_font():
    return FontFamily.objects.get(id=1)


class Text(Block):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators += []

    text = models.TextField(blank=False)
    font_size = models.IntegerField(
        default=12, validators=[MinValueValidator(1), MaxValueValidator(200)]
    )
    font_family = models.ForeignKey(
        FontFamily,
        default=get_default_font,
        on_delete=models.SET_DEFAULT,
    )

    def __str__(self):
        return f"text on {self.site.name}"


class Image(BaseMediaModel, Block):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators += []

    def __str__(self):
        return f"image on {self.site.name}"


class Slider(Block):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators += []


class SlideImage(BaseMediaModel):
    slider = models.ForeignKey(Slider, related_name="slides", on_delete=models.CASCADE)


class Iframe(Block):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators += []

    origin = models.URLField(max_length=255)

    def __str__(self):
        return f"{self.origin} on {self.site.name}"
