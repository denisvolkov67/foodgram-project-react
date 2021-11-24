from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)

    def __str__(self):
        return '{}, {}'.format(self.name, self.unit)


class Recipe(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    cooking_time = models.PositiveIntegerField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe'
    )


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()
