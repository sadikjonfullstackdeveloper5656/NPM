from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    contact = models.EmailField()
    address = models.CharField(max_length=1024)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField(to="Product", related_name="orders")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.customer} - {self.total_price}"


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", null=True)
    in_stock = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.price}"

    class Meta:
        ordering = ['-id']


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
