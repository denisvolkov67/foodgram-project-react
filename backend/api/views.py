from rest_framework import viewsets

from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer
)
from api.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from recipes.models import Ingredient, Recipe, Tag


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    search_fields = ('name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
