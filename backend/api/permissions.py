from rest_framework import permissions


class AuthForItemOrReadOnly(permissions.BasePermission):
    """
    Позволяет просматривать список объектов и создавать объект всем,
    аутентифицированным просматривать объект.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.method in permissions.SAFE_METHODS
            or request.method == 'POST'
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated


class AuthorOrAuthOrReadOnly(permissions.BasePermission):
    """
    Позволяет просматривать список объектов и объект всем,
    аутентифицированным создавать объект,
    автору изменять и удалять объект.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        if request.method in ("PATCH", "DELETE"):
            return obj.author == request.user
        return True
