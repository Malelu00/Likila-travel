from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Read access for everyone (public API).
    Write access only for authenticated admin users.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsAdminUser(BasePermission):
    """Only staff/admin users."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff
