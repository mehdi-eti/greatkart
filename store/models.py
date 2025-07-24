from django.db import models
from django.urls import reverse

from category.models import Category


# Create your models here.


class Products(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=255, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self) -> str:
        return self.product_name


class VariationManager(models.Manager):
    def color(self):
        return super(VariationManager, self).filter(veriation_category='color', is_active=True)

    def size(self):
        return super(VariationManager, self).filter(veriation_category='size', is_active=True)


class Veriation(models.Model):
    variation_category_choice = (
        ('color', 'Color'),
        ('size', 'Size'),
    )
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    veriation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self) -> str:
        return self.variation_value
