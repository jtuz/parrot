from django.urls import path

from orders.views import (
    OrderView,
    TopProductView
)

app_name = 'orders'

urlpatterns = [
    path('sells/', TopProductView.as_view()),
    path('order/', OrderView.as_view()),
]
