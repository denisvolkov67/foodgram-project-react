from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientViewSet, 'ingredients')
router.register(r'tags', TagViewSet, 'tags')
router.register(r'recipes', RecipeViewSet, 'recipes')

urlpatterns = [
    path('', include('users.urls')),
    path('', include(router.urls)),
]
