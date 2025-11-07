from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admins to edit, but anyone can read.
    """

    def has_permission(self, request, view):
        # SAFE_METHODS are GET, HEAD, and OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for admin users
        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ "
    Custom permission to allow any authenticated user to create objects,
    and edit or delete their own objects.
    Unauthenticated users can only view a list of objects.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
