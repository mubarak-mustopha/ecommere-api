from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Category, ColorVariant, SizeVariant, Product
from .serializers import (
    CategorySerializer,
    ColorVariantSerializer,
    SizeVariantSerializer,
    ProductSerializer,
)


# Create your views here.
class BaseAdminAPIViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.ViewSet,
):
    permission_classes = [IsAuthenticated, IsAdminUser]


class CategoryAdminAPIViewSet(BaseAdminAPIViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = [FormParser, MultiPartParser]


class ColorVariantAdminAPIViewSet(BaseAdminAPIViewSet):
    queryset = ColorVariant.objects.all()
    serializer_class = ColorVariantSerializer


class SizeVariantAdminAPIViewSet(BaseAdminAPIViewSet):
    queryset = SizeVariant.objects.all()
    serializer_class = ColorVariantSerializer


class ProductAdminAPIViewSet(BaseAdminAPIViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
