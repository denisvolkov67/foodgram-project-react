from django.urls import include, path
from rest_framework import routers

from .views import (UserViewSet)

v1_router = routers.DefaultRouter()
v1_router.register(r"users", UserViewSet, "users")
# v1_router.register(r"auth/token/login", LoginViewSet, "login")
# v1_router.register(r"auth/token/logout", LogoutViewSet, "logout")

urlpatterns = [
    path("", include(v1_router.urls)),
]
