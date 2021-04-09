from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        blank=False
    )
    price = models.FloatField()

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Product, self).save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.CASCADE
    )
    customer_name = models.CharField(max_length=200, blank=False)
    created_at = models.DateTimeField(
        editable=False,
        blank=True,
        auto_now_add=True
    )

    @property
    def total(self):
        return sum([item.quantity * item.product.price for item in OrderItem.objects.filter(order=self)])


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
