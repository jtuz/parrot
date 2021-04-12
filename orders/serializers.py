
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.db.utils import IntegrityError

from orders.models import Product, Order, OrderItem


class OrderSerializer(serializers.BaseSerializer):

    def to_internal_value(self, data):
        user = data.user
        customer_name = data.data.get('customer_name')
        order_items = data.data.get('order_items')

        # Perform the data validation.
        if not customer_name:
            raise ValidationError({
                'customer_name': 'Este campo es requerido'
            })
        if not order_items:
            raise ValidationError({
                'order_items': 'Al menos un pedido debe de estar en la orden'
            })

        return {
            'user': user,
            'customer_name': customer_name,
            'order_items': order_items,
            'total': None
        }

    def to_representation(self, obj):
        return {
            'waiter': f"{obj.user.first_name}",
            'customer_name': obj.customer_name,
            'total': obj.total
        }

    def create(self, validated_data):
        order = Order.objects.create(
            user=validated_data['user'],
            customer_name=validated_data['customer_name']
        )
        for item in validated_data['order_items']:
            OrderItem.objects.create(
                order=order,
                product=self._check_inventory(item['product'], item['price']),
                quantity=item['quantity']
            )

        return order

    def _check_inventory(self, product, price):
        current_product = None
        try:
            current_product = Product.objects.create(
                name=product,
                price=price
            )
        except IntegrityError:
            current_product = Product.objects.get(name=product.upper())

        return current_product


class TopProdutSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(read_only=True)
    total_sells = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ('product_name', 'total_sells')
