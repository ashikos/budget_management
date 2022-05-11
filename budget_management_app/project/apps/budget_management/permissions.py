from rest_framework import permissions , exceptions
from apps.budget_management import constants
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
        allows only users , if not safe method , user model,
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class IsUserOrReadOnly(permissions.BasePermission):
    """
        Checks wheather object is users or not
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id


class UserFromToken(permissions.BasePermission):
    """
     identifying user from Token
    """

    def has_permission(self, request, view):
        auth = get_authorization_header(request).split()
        var = str(auth.pop(1), 'utf-8')
        # print(var)
        # print(type(Token.objects.first().key))
        user = Token.objects.get(key=var).user
        view.kwargs['user'] = user
        return True


class IsAdminOrMember(permissions.BasePermission):
    """
        permission for editing only to admin
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.type != constants.user_type_admin:
            raise exceptions.ValidationError('you are not an admin')

        return True
