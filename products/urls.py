from django.urls import path
from rest_framework.routers import DefaultRouter


from .views import (
    CategoryAdminAPIViewSet,
    ColorVariantAdminAPIViewSet,
    ProductAdminAPIViewSet,
    SizeVariantAdminAPIViewSet,
)

router = DefaultRouter()
router.register("admin/colors", ColorVariantAdminAPIViewSet, basename="color")
router.register("admin/sizes", SizeVariantAdminAPIViewSet, basename="size")
router.register("admin/categorys", CategoryAdminAPIViewSet, basename="category")
router.register("admin/products", ProductAdminAPIViewSet, basename="category")

urlpatterns = router.urls
