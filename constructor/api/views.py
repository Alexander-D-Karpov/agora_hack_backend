from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser

from constructor.api.serializers import (
    FontFamilySerializer,
    FullTextBlockSerializer,
    SiteSerializer,
    ImageBlockSerializer,
    SliderBlockSerializer,
    SlideImageSerializer,
)
from constructor.models import FontFamily, Site


class ListCreateSiteApiView(generics.ListCreateAPIView):
    serializer_class = SiteSerializer

    def get_queryset(self):
        return Site.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListCreateFontsApiView(generics.ListCreateAPIView):
    serializer_class = FontFamilySerializer

    def get_queryset(self):
        return FontFamily.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CreateTextBlockApiView(generics.CreateAPIView):
    serializer_class = FullTextBlockSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CreateImageBlockApiView(generics.CreateAPIView):
    serializer_class = ImageBlockSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AddSlideImageApiView(generics.CreateAPIView):
    serializer_class = SlideImageSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CreateSlideBlockApiView(generics.CreateAPIView):
    serializer_class = SliderBlockSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
