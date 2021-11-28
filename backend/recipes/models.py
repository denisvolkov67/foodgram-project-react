from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return '{}, {}'.format(self.name, self.measurement_unit)


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    color = models.CharField(max_length=7, verbose_name="Цвет в HEX")
    slug = models.SlugField(
        max_length=200,
        verbose_name="Уникальный слаг",
        unique=True
    )

    def __str__(self):
        return '{}, {}'.format(self.name, self.color)


class Recipe(models.Model):
    name = models.CharField(max_length=200, null=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes", null=True
    )
    text = models.TextField(null=True)
    cooking_time = models.PositiveIntegerField()
    # image=
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe'
    )
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()
