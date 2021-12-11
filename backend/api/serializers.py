from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag)
from users.models import Follow
from users.serializers import CustomUserSerializer

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientRecipe.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        read_only_fields = ('author', 'tags',)

    def get_ingredients(self, obj):
        queryset = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        try:
            request = self.context['request']
            user = request.user
            return (Recipe.objects.filter(favorites__user=user, id=obj.id)
                    .exists())
        except (TypeError, KeyError):
            return False

    def get_is_in_shopping_cart(self, obj):
        try:
            request = self.context['request']
            user = request.user
            return Recipe.objects.filter(cart__user=user, id=obj.id).exists()
        except (TypeError, KeyError):
            return False

    def create_ingredients(self, ingredients, recipe):
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(
                Ingredient, id=ingredient_item.get('id')
            )
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=ingredient_item.get('amount'),
            )

    def validate(self, data):
        tags = self.initial_data.get("tags")
        if not tags:
            raise serializers.ValidationError(
                "Убедитесь, что добавлен хотя бы один тег"
            )
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError("Теги должны быть уникальными")
        data["tags"] = tags

        ingredients = self.initial_data.get("ingredients")
        if not ingredients or len(ingredients) < 1:
            raise serializers.ValidationError(
                "Нужен хоть один ингридиент для рецепта"
            )
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(
                Ingredient, id=ingredient_item["id"]
            )
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    "Ингридиенты должны быть уникальными"
                )
            ingredient_list.append(ingredient)
            if int(ingredient_item["amount"]) <= 0:
                raise serializers.ValidationError(
                    "Убедитесь, что значение количества ингредиента больше 0"
                )
        data["ingredients"] = ingredients

        cooking_time = self.initial_data.get("cooking_time")
        if not int(cooking_time) > 0:
            raise serializers.ValidationError(
                "Убедитесь, что время приготовления больше нуля"
            )
        data["cooking_time"] = cooking_time
        return data

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(ingredients_data, recipe)
        recipe.tags.set(tags_data)
        return recipe

    def update(self, recipe, validated_data):
        if "ingredients" in self.initial_data:
            ingredients = validated_data.pop("ingredients")
            recipe.ingredients.clear()
            self.create_ingredients(ingredients, recipe)
        if "tags" in self.initial_data:
            tags_data = validated_data.pop("tags")
            recipe.tags.set(tags_data)
        return super().update(recipe, validated_data)


class SubscriptionsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count')

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return RecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()


class FollowSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()
    user = serializers.PrimaryKeyRelatedField(queryset=queryset)
    author = serializers.PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model = Follow
        fields = ('user', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author')
            )
        ]

    def validate(self, data):
        request = self.context.get('request')
        author = data['author']
        if request.user == author:
            raise serializers.ValidationError('Нельзя подписаться на себя')
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return SubscriptionsSerializer(instance, context=context).data


class CartSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Cart
        fields = ('id', 'name', 'image', 'cooking_time', 'user', 'recipe')

    def validate(self, data):
        if Cart.objects.filter(user=data['user'],
                               recipe=data['recipe']).exists():
            raise serializers.ValidationError(
                'Рецепт есть в списке покупок.')
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time', 'user', 'recipe')
