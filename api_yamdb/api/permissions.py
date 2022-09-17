from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    The permission grants access only to the superuser or admin.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    The permission grants access to the superuser, admin or read only.
    """

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """
    The permission grants access to the superuser, admin, moderator,
    author or read only.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )
