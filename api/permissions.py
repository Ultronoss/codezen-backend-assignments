from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Admins can access any object
        if request.user.is_staff:
            return True
        # Otherwise, only the owner can access
        return obj.customer.user == request.user
