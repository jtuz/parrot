from django.db import models
from django.db.models import F, Sum
from django.db.models.functions import Upper
from django.contrib.auth.models import User


class ProductManager(models.Manager):
    def top(self):
        return (
            OrderItem
            .objects
            .values(product_name=Upper('product__name'))
            .annotate(total_sells=Sum('quantity'))
            .order_by('-total_sells')
        )


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        blank=False
    )
    price = models.FloatField()
    objects = ProductManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Product, self).save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.CASCADE
    )
    customer_name = models.CharField(
        max_length=200,
        blank=False
    )
    created_at = models.DateTimeField(
        editable=False,
        blank=True,
        auto_now_add=True
    )

    @property
    def total(self):
        return self.items.all().aggregate(
            total=Sum(
                F('quantity') * F('product__price'),
                output_field=models.FloatField())
        )['total']


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='in_orders',
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
