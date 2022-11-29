from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import CreatedModel
from recipes.models import Recipe


class User(AbstractUser):
    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='Ник пользователя',
        db_index=True,
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия пользователя',
    )
    is_favorited = models.ManyToManyField(
        Recipe,
        related_name='favorited',
        blank=True,
    )
    is_in_shopping_cart = models.ManyToManyField(
        Recipe,
        related_name='shopping_cart',
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'password', ]

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username


class Follow(CreatedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_following')
        ]
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
