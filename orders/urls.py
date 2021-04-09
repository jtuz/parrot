#  from rest_framework import routers
from django.urls import include, path

from orders.views import (
    OrderView,
    TopProductViewSet
)

#  router = routers.DefaultRouter()
#  router.register(r'sells', TopProductViewSet)

app_name = 'orders'

urlpatterns = [
    #  path('', include(router.urls)),
    path('order/', OrderView.as_view()),
    path('sells/', TopProductViewSet.as_view())
]
