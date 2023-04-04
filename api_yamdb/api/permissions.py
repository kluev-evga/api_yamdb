from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.role == 'admin')
        )


class AdminModeratorOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and (
                        request.user.is_superuser
                        or request.user.role == 'admin'
                        or request.user.role == 'moderator'
                        or obj.author_id == request.user.pk))


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return (request.user
                and request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == 'admin'))


class AnyAuthorized(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.user
                and request.user.is_authenticated
                and (obj.username == request.user.username
                     or request.user.is_superuser
                     or request.user.role == 'admin'
                     or request.user.role == 'moderator'))
