from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Tag


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):

    def favorite_count_field(self, obj):
        return obj.favorited.count()
    favorite_count_field.short_description = ('Количество добавлений '
                                              'рецепта в избранное')

    list_display = (
        'pk',
        'name',
        'author',
    )

    search_fields = (
        'name',
        'author',
    )

    list_filter = (
        'author',
        'tags',
        'name',
    )
    inlines = (RecipeIngredientInline,)
    filter_horizontal = ('tags',)
    readonly_fields = ('favorite_count_field',)
    fieldsets = (
        (None, {"fields": ('name',
                           "author",
                           "image",
                           "text",
                           "tags",
                           "cooking_time",
                           "favorite_count_field")}),
    )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
        'pub_date',
    )

    search_fields = (
        'name',
    )

    list_filter = (
        'pub_date',
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    list_filter = (
        'pk',
        'name',
        'measurement_unit',
        'pub_date'
    )

    search_fields = (
        'name',
    )

    list_filter = (
        'pub_date',
    )
    inlines = (RecipeIngredientInline,)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'amount',
    )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
