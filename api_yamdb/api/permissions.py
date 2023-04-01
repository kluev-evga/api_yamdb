from rest_framework.permissions import BasePermission


class IsOwnerOrIsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.username == request.username or request.user.is_staff
