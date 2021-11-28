from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, RecipeViewSet, TagViewSet


v1_router = routers.DefaultRouter()
v1_router.register(r"ingredients", IngredientViewSet, "ingredients")
v1_router.register(r"tags", TagViewSet, "tags")
v1_router.register(r"recipes", RecipeViewSet, "recipes")

urlpatterns = [
    path('v1/', include('users.urls')),
    path('v1/', include(v1_router.urls)),
]
