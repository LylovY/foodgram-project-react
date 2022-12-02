from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Follow, User


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ('username', "email", "password")}),
        (("Личные данные"), {"fields": ("first_name", "last_name")}),
        (("Подписки"), {"fields": ("is_favorited", "is_in_shopping_cart")}),
        (("Полномочия"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ('id', 'username', 'email',)
    list_filter = ('username', 'email',)
    empty_value_display = '-пусто-'
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )

    search_fields = (
        'username',
        'email',
    )


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author',
    )


admin.site.register(Follow, FollowAdmin)
