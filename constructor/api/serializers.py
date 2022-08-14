from colorfield.serializers import ColorField
from rest_framework import serializers

from constructor.models import Text, FontFamily


class BaseBlockSerializer(serializers.Serializer):
    # Need to re-declare fields since this is not a ModelSerializer
    margin_right = serializers.CharField(max_length=20)
    margin_left = serializers.CharField(max_length=20)
    margin_bottom = serializers.CharField(max_length=20)
    margin_top = serializers.CharField(max_length=20)

    padding_right = serializers.CharField(max_length=20)
    padding_left = serializers.CharField(max_length=20)
    padding_bottom = serializers.CharField(max_length=20)
    padding_top = serializers.CharField(max_length=20)

    width = serializers.CharField(max_length=20)
    height = serializers.CharField(max_length=20)

    background_color = ColorField(required=True)
    color = ColorField(required=True)

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


class FullTextBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = BaseBlockSerializer.Meta.fields + ["text", "font_size", "font_family"]
