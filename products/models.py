from django.db import models


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    parent_cat = models.ForeignKey(
        to="self", on_delete=models.SET_NULL, related_name="sub_cats", null=True
    )
    image = models.ImageField(upload_to="categories")

    def __str__(self):
        return self.title


class ColorVariant(models.Model):
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.value


class SizeVariant(models.Model):
    value = models.CharField(max_length=5)

    def __str__(self):
        return self.value


class Product(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="products")
    price = models.DecimalField(max_digits=14, decimal_places=6)
    description = models.TextField(blank=True)
    in_stock = models.PositiveIntegerField(default=5)

    category = models.ForeignKey(
        to=Category, on_delete=models.CASCADE, related_name="products"
    )
    colors = models.ManyToManyField(to=ColorVariant, blank=True)
    sizes = models.ManyToManyField(SizeVariant, through="ProductSize")

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeVariant, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=14, decimal_places=6)
    in_stock = models.PositiveIntegerField(default=5)

    def __str__(self):
        return f"<{self.product}: {self.size}>"
