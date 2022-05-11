from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser, \
    AbstractBaseUser
from apps.budget_management.constants import user_type_choices, user_type_member
from apps.budget_management.constants import \
    user_type_account, account_type_savings, account_type_income, \
    user_type_category, user_type_admin
from django.utils import timezone


# class MyUserManager(BaseUserManager):
#     """
#     For customizing the user model
#     """
#
#     def create_user(self, email, username, phone, type, password=None):
#         user = self.model(
#             username=username,
#             email=self.normalize_email(email),
#             phone=phone,
#             type=type,
#         )
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user


# def create_superuser(self, email, username, phone, password=None):
#     user = self.create_user(
#
#         email=self.normalize_email(email),
#         password=password,
#         phone=phone,
#         username=username,
#         user_type=user_type_admin
#     )
#
#     user.is_superuser = True
#     user.is_staff = True
#     user.save()
#
#     return user


class CustomUser(AbstractUser, PermissionsMixin, ):
    """
    USER
        username : (char) username of user
        email : (email) email of user
        password : (char) password which is used for login purpose
        phone : (int) contact of user which is used to login purposes
        user_type : (int) to know whether user is a admin or user
    """

    # username = models.CharField(max_length=30)
    # email = models.EmailField(max_length=220, unique=True)
    # password = models.CharField(max_length=225)
    phone = models.CharField(max_length=25, unique=True)
    type = models.IntegerField(default=user_type_member,
                               choices=user_type_choices,
                               )

    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)

    # objects = MyUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']



    # def __str__(self):
    #     return f'{self.username}, {self.get_type_display()}'

    def __str__(self):
        return self.username

    @property
    def get_address(self):
        return  self.username+self.phone


    # def set_password(self, password):
    #     self.set_password(password)
    #     """ using= : used in case of multiple databases """
    #     self.save()
    #     return True


class Family(models.Model):
    """
    group containing one or more members
        name :(char) name of group
        users : (manytomany) members of the group
    """
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(CustomUser)
    income = models.IntegerField(default=0)
    expanse = models.IntegerField(default=0)


class Account(models.Model):
    """
    user account details
        user: (fk) account holder
        amount :(int)amount in the account
        type : (int) whether account is current , savings, fixed
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE ,related_name='account')
    amount = models.IntegerField()
    type = models.IntegerField(
        default=account_type_savings, choices=user_type_account, )

    def __str__(self):
        return self.user.username


class Transaction(models.Model):
    """
    Data of Transaction made by the user
        user  (fk): name of user
        account  (fk) :account_id of user
        category  (int): whether it's an income or expanse
        amount (int): amount of transaction
        date  (date): date of transaction
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account = models.IntegerField(
        default=account_type_savings, choices=user_type_account)
    category = models.IntegerField(
        default=account_type_income, choices=user_type_category)
    note = models.TextField()
    amount = models.IntegerField()
    date = models.DateField(default=timezone.now)
