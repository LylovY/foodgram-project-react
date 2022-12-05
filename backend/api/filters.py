import django_filters
from recipes.models import Recipe, Tag, Ingredient
from users.models import User
from rest_framework import filters


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all())
    author = django_filters.filters.ModelChoiceFilter(
        queryset=User.objects.all())
    is_favorited = django_filters.CharFilter(
        method='filter_is_favorited',
    )
    is_in_shopping_cart = django_filters.CharFilter(
        method='filter_is_in_shopping_cart',
    )

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value == '1':
            return queryset.filter(favorited=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == '1':
            return queryset.filter(shopping_cart=user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

