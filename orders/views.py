from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response


from orders.models import Product

from rest_framework import (
    status,
    permissions
)

from orders.serializers import (
    OrderSerializer,
    TopProdutSerializer
)


class TopProductView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.top()
    serializer_class = TopProdutSerializer


class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
