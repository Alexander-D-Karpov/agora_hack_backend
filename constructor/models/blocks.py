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

    type = "Text"

    text_block = models.TextField(blank=False)
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

    def get_json(self):
        json = {
            "text": self.text_block,
            "font_size": self.font_size,
            "font_family": self.font_family.file.url,
        }
        json.update(self._get_base_json())
        return json


class Image(BaseMediaModel, Block):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators += []

    type = "Image"

    def get_json(self):
        json = {"image": self.image}
        json.update(self._get_base_json())
        return json

    def __str__(self):
        return f"image on {self.site.name}"


class Slider(Block):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators += []

    type = "Slider"

    def get_json(self):
        json = {
            "slides": [x.file.url for x in self.slides.all()],
        }
        json.update(self._get_base_json())
        return json


class SlideImage(BaseMediaModel):
    slider = models.ForeignKey(Slider, related_name="slides", on_delete=models.CASCADE)

    def slider_slug(self):
        # TODO make SerializerMethodField in serializer
        pass


class Iframe(Block):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators += []

    type = "Iframe"

    origin = models.URLField(max_length=255)

    def get_json(self):
        json = {
            "origin": self.origin,
        }
        json.update(self._get_base_json())
        return json

    def __str__(self):
        return f"{self.origin} on {self.site.name}"


class Row(Block):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators += []

    type = "Row"
    is_parent = True

    def get_json(self):
        json = {
            "blocks": [x.get_json() for x in self.children.all()],
        }
        json.update(self._get_base_json())
        return json

    def __str__(self):
        return f"row on {self.site.name}"


class Column(Block):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators += []

    type = "Column"
    is_parent = True

    def get_json(self):
        json = {
            "blocks": [x.get_json() for x in self.children.all()],
        }
        json.update(self._get_base_json())
        return json

    def __str__(self):
        return f"column on {self.site.name}"
