from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission class to allow object access only to the owner or for read-only methods.

    This permission ensures that:
    - Safe methods (e.g., GET, HEAD, OPTIONS) are always allowed.
    - Write permissions are only granted if the requesting user is the owner of the object.

    Methods:
        has_object_permission(request, view, obj):
            Checks if the request method is safe or if the requesting user is the owner of the object.

    Args:
        request: The HTTP request object.
        view: The view being accessed.
        obj: The object being accessed.

    Returns:
        bool: True if the request is allowed, False otherwise.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user