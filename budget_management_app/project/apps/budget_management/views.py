from django.http import request
from rest_framework import viewsets, status, filters
from apps.budget_management.models import CustomUser, Family, Account, \
    Transaction
from apps.budget_management import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from apps.budget_management import permissions, models ,search
from django_filters.rest_framework import DjangoFilterBackend

class UserViewSet(viewsets.ModelViewSet):
    """
    User
        purpose :for listing ,posting , updating, and deleting
        all other fields can be used only after creating a user profile
    """
    permission_classes = (permissions.IsOwnerOrReadOnly,)
    queryset = CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    authentication_classes = (TokenAuthentication,)
    #filter_backends = (DjangoFilterBackend,)

    filterset_class = search.UserFilter
    #search_fields = ('username',)

class FamilyViewSet(viewsets.ModelViewSet):
    """
    Family
        Family or group can be created,
        users can be added to this family,
        purpose :for listing ,posting , updating, and deleting
    """

    permission_classes = (IsAuthenticated, permissions.IsAdminOrMember,)
    serializer_class = serializers.FamilySerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        try:
            var = Family.objects.filter(users=user)
        except Exception as e:
            print('@@@@@@@',e)
        return var


class AccountViewSet(viewsets.ModelViewSet):
    """
    ACCOUNT DETAILS
        user account details
        purpose :for listing ,posting , updating, and deleting
    """

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(user=user)

    serializer_class = serializers.AccountSerializer
    permission_classes = (IsAuthenticated,
                          permissions.IsUserOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        """for adding owner to the Account model"""
        serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    TRANSACTIONS
        purpose :for listing ,posting , updating, and deleting transaction
         details
    """
    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user)

    serializer_class = serializers.TransactionSerializer
    permission_classes = (
        IsAuthenticated, permissions.IsUserOrReadOnly,)

    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        """for adding owner to the Transaction model"""
        serializer.save(user=self.request.user)


class LoginView(ObtainAuthToken):
    """
    LOGIN
        provides token to users on submitting required credentials.
        credentials : phone & Password
    """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
