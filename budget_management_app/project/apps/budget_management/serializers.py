from rest_framework import serializers, status
from apps.budget_management import models
from apps.budget_management import constants
from rest_framework.exceptions import NotFound
from django.db.models import Sum, Avg
from rest_framework.response import Response
from django.http import JsonResponse
from django.core import serializers as django_serializers


"""
    serializer for user model
    override create and update function for password hashing
"""


class UserSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField(
        'get_address',
        )

    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True)

    def get_address(self, obj):
        return obj.username + obj.email


    class Meta:
        model = models.CustomUser
        fields = ['id', 'username', 'email', 'phone', 'password', 'type',
                  'address']

    def create(self, validated_data):
        # user = models.CustomUser.objects.create_user(
        #     email=validated_data['email'],
        #     username=validated_data['username'],
        #     password=validated_data['password'],
        #     phone=validated_data['phone'],
        #     type=constants.user_type_member
        # )
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

    # def to_representation(self, instance ):
    #     data = super(UserSerializer, self).to_representation(instance)
    #
    #     data['address']=data['username']+data['email']
    #     print(data)
    #     return data


"""
serializer for Family model
"""


class FamilySerializer(serializers.ModelSerializer):
    income = serializers.IntegerField(
        read_only=True,
    )
    expanse = serializers.IntegerField(
        read_only=True,
    )

    # users = serializers.SerializerMethodField('get_users')
    #
    # def get_users(self,obj):
    #     user = self.context['request'].user
    #     users = models.CustomUser.objects.exclude(username=user)
    #
    #     users_list=[]
    #
    #     for user in users:
    #         user_data = UserSerializer(user).data
    #         users_list.append(user_data)
    #
    #
    #     print(users_list)
    #     return users_list


    class Meta:
        model = models.Family
        fields = ['id', 'name', 'users', 'income', 'expanse']

    def create(self, validated_data):
        user = self.context['request'].user

        if user not in validated_data['users']:
            validated_data['users'].append(user)

        # for user in validated_data['users']:

        total_amount = models.Account.objects.filter(
            user__in=validated_data['users']).aggregate(
            total_amount=Sum('amount'))['total_amount']


        validated_data['income'] = total_amount
        print(total_amount)

        #return super().create(validated_data)


"""
serializer for Account 
override create function for checking weather account exits
"""


class AccountSerializer(serializers.ModelSerializer):
    user = serializers.CharField(
        read_only=True,
    )

    class Meta:
        model = models.Account
        fields = ['id', 'user', 'type', 'amount']

    def create(self, validated_data):
        """
        Checking whether account exist or not using user and account data
        """
        if models.Account.objects.filter(user=validated_data['user'],
                                         type=validated_data['type']).exists():
            raise serializers.ValidationError(
                'account already exist     ')

        # return super().create(validated_data)


"""
serializer for transaction
override create for updating Account model 
total income and expanse of family is updated
"""


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.CharField(

        read_only=True
    )

    class Meta:
        model = models.Transaction
        fields = ['id', 'user', 'account', 'category', 'note', 'amount', 'date']

    def create(self, validated_data):
        try:
            account_obj = models.Account.objects.get(
                user=validated_data['user'], type=validated_data['account'])

        except:
            raise NotFound('account not exists')

        try:
            family_obj = models.Family.objects.get(
                users=validated_data['user'])
        except:
            family_obj = None

        amount = account_obj.amount

        if validated_data['category'] == constants.account_type_income:
            current_balance = amount + validated_data['amount']
            account_obj.amount = current_balance
            account_obj.save()

            # data = {
            #     'amount': current_balance
            # }
            # account_detail = AccountSerializer(
            #     account_obj, data=data, partial=True)
            # if account_detail.is_valid(raise_exception=True):
            #     account_detail.save()

            """
                updating family income
            """
            if family_obj:
                income = family_obj.income
                current_income = income + validated_data['amount']
                family_obj.income = current_income
                family_obj.save()


        elif validated_data['category'] == constants.account_type_expanse:
            # print('@@@@@@@@@@', validated_data['category'], amount)
            current_balance = amount - validated_data['amount']
            account_obj.amount = current_balance
            account_obj.save()

            """
            updating family expanse
            """
            if family_obj:
                expanse = family_obj.expanse
                current_expanse = expanse + validated_data['amount']
                family_obj.expanse = current_expanse
                family_obj.save()

        return super().create(validated_data)
