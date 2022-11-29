from django.db import models
from django.core.validators import (MinLengthValidator, MinValueValidator)

from core.models import CreatedNameModel, CreatedModel


class Recipe(CreatedNameModel):

    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Изображение',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        validators=[MinLengthValidator(1, 'Пустое поле')]
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        related_name='recipes',
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Теги',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(1, 'Минимальное время 1 м.')],
    )

    class Meta:
        verbose_name = 'Рецепты'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']


class Tag(CreatedNameModel):

    color = models.CharField(
        max_length=16,
        verbose_name='Цвет',
    )
    slug = models.SlugField(
        verbose_name='slug'
    )

    class Meta:
        verbose_name = 'Тэги'
        verbose_name_plural = 'Теги'
        ordering = ['-pub_date']


class Ingredient(CreatedNameModel):

    measurement_unit = models.CharField(
        max_length=10,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиенты'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['-pub_date']


class RecipeIngredient(CreatedModel):
    reciepe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes_ingredient',
        verbose_name='Рецепт'
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_recipe',
        verbose_name='Ингредиент'
    )

    amount = models.FloatField(
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиент рецепта'
        ordering = ['-pub_date']
