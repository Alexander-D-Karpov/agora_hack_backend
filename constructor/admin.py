from django.contrib import admin

from .models import FontFamily, Text, Image, Slider, Iframe, SlideImage

admin.site.register(FontFamily)
admin.site.register(Text)
admin.site.register(Image)
admin.site.register(Slider)
admin.site.register(Iframe)
admin.site.register(SlideImage)
