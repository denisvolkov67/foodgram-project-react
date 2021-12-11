from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return '{}, {}'.format(self.name, self.measurement_unit)


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    color = ColorField('Цвет в HEX', default='#00FF00')
    slug = models.SlugField(
        max_length=200,
        verbose_name='Уникальный slug',
        unique=True
    )

    def __str__(self):
        return '{}, {}'.format(self.name, self.color)


class Recipe(models.Model):
    name = models.CharField(max_length=200, null=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes', null=True
    )
    text = models.TextField(null=True)
    cooking_time = models.PositiveIntegerField()
    image = models.ImageField(null=True, upload_to='recipes/')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe'
    )
    tags = models.ManyToManyField(Tag)
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                1, message='Минимальное время приготовления 1 минута'),))

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return str(self.ingredient)


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
    )

    def __str__(self):
        return '{}, {}'.format(self.user.username, self.recipe.name)


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
