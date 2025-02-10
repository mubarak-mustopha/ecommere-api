import re
from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer

from .models import Category, ColorVariant, SizeVariant, Product, ProductSize


def normalize(value):
    return re.sub(r"([^a-zA-Z]|\s)+", " ", value)


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class ColorVariantSerializer(ModelSerializer):

    class Meta:
        model = ColorVariant
        fields = ["value"]

    def validate_value(self, value):
        value = re.sub(r"\s+", " ", value)
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError(
                "value should contain only alphabets (optionally separated with spaces)"
            )
        return value.capitalize()

    def save(self, **kwargs):
        value = self.validated_data["value"]
        filtered_qs = ColorVariant.objects.filter(slug=slugify(value))

        # for updates
        if self.instance:
            filtered_qs = filtered_qs.exclude(id=self.instance.id)

        if filtered_qs.exists():
            raise serializers.ValidationError(
                f"A color variant with value `{value}` already exists"
            )
        return super().save(**kwargs)


class SizeVariantSerializer(ModelSerializer):

    class Meta:
        model = SizeVariant
        fields = ["value"]

    def validate_value(self, value):
        value = re.sub(r"\s+", " ", value)
        if not value.replace(" ").isalpha():
            raise serializers.ValidationError("value should contain only alphabets")

        return value.capitalize()


class ProductSizeSerializer(ModelSerializer):
    class Meta:
        model = ProductSize
        exclude = ["product"]


class ProductSerializer(ModelSerializer):
    colors = ColorVariantSerializer(many=True, required=False)
    sizes = ProductSizeSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = "__all__"
        # exclude = ["colors", "sizes"]

    def create(self, **validated_data):
        colors = validated_data.pop("colors", [])
        sizes = validated_data.get("sizes", [])

        product = super().create(**validated_data)

        for color in colors:
            pass
