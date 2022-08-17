from colorfield.serializers import ColorField
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from constructor.models import Text, FontFamily, Site, Image, Block, Slider, SlideImage


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ["name"]

    def create(self, validated_data):
        return Site.objects.create(**validated_data, user=self.context["request"].user)


class BaseBlockSerializer(serializers.Serializer):
    # Need to re-declare fields since this is not a ModelSerializer
    margin_right = serializers.CharField(max_length=20, default="none")
    margin_left = serializers.CharField(max_length=20, default="none")
    margin_bottom = serializers.CharField(max_length=20, default="none")
    margin_top = serializers.CharField(max_length=20, default="none")

    padding_right = serializers.CharField(max_length=20, default="none")
    padding_left = serializers.CharField(max_length=20, default="none")
    padding_bottom = serializers.CharField(max_length=20, default="none")
    padding_top = serializers.CharField(max_length=20, default="none")

    width = serializers.CharField(max_length=20, default="none")
    height = serializers.CharField(max_length=20, default="none")

    background_color = ColorField(default="#232325")
    color = ColorField(default="#6385b5")

    class Meta:
        fields = [
            "margin_right",
            "margin_left",
            "margin_bottom",
            "margin_top",
            "padding_right",
            "padding_left",
            "padding_bottom",
            "padding_top",
            "width",
            "height",
            "background_color",
            "color",
        ]

    def _get_site(self):
        site = get_object_or_404(
            Site, name=self.context["request"].parser_context["kwargs"]["slug"]
        )
        if site.user != self.context["request"].user:
            raise AuthenticationFailed("You are not allowed to edit this site")
        return site

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError


class FontFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = FontFamily
        fields = ["id", "file"]
        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):
        return FontFamily.objects.create(
            **validated_data,
            name=validated_data["file"].name,
            user=self.context["request"].user
        )


class FullTextBlockSerializer(serializers.ModelSerializer, BaseBlockSerializer):
    class Meta:
        model = Text
        fields = BaseBlockSerializer.Meta.fields + [
            "slug",
            "text",
            "font_size",
            "font_family",
        ]
        extra_kwargs = {"slug": {"read_only": True}}

    def create(self, validated_data):
        return Text.objects.create(**validated_data, site=self._get_site())


class ImageBlockSerializer(serializers.ModelSerializer, BaseBlockSerializer):
    file = serializers.ImageField(required=True)

    class Meta:
        model = Image
        fields = BaseBlockSerializer.Meta.fields + [
            "slug",
            "file",
        ]
        extra_kwargs = {"slug": {"read_only": True}}

    def create(self, validated_data):
        return Image.objects.create(
            **validated_data, site=self._get_site(), user=self.context["request"].user
        )


class SliderBlockSerializer(serializers.ModelSerializer, BaseBlockSerializer):
    class Meta:
        model = Slider
        fields = BaseBlockSerializer.Meta.fields + [
            "slug",
        ]
        extra_kwargs = {"slug": {"read_only": True}}

    def create(self, validated_data):
        return Slider.objects.create(**validated_data, site=self._get_site())


class SlideImageSerializer(serializers.ModelSerializer):
    slider_slug = serializers.SlugField(required=True)
    file = serializers.ImageField(required=True)

    class Meta:
        model = SlideImage
        fields = ["slider_slug", "file"]
        extra_kwargs = {"slider_slug": {"write_only": True}}

    def create(self, validated_data):
        slider = get_object_or_404(Slider, slug=validated_data["slider_slug"])

        if slider.site.user != self.context["request"].user:
            raise AuthenticationFailed("You are not allowed to edit this site")

        return SlideImage.objects.create(
            file=validated_data["file"],
            user=self.context["request"].user,
            slider=slider,
        )
