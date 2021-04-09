from rest_framework import routers
from django.urls import include, path

from parrot_auth.views import (
    UserView,
    UserViewSet
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

app_name = 'parrot_auth'

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserView.as_view())
]
