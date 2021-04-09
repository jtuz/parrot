from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from rest_framework import (
    status,
    viewsets,
    permissions
)

from orders.serializers import (
    OrderSerializer
)


class TopProductViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT p.name,SUM(I.quantity) as total_vendidos
            FROM orders_order O
            JOIN orders_orderitem I ON O.id=I.order_id
            LEFT JOIN orders_product P ON I.product_id=P.id
            GROUP BY p.name
            ORDER BY total_vendidos DESC;
            """
        )
        rows = cursor.fetchall()

        top_products = [{"product": row[0], "total_sell": row[1]} for row in rows]

        return Response(top_products)


class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
