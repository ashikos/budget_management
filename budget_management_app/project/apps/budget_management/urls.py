# from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from apps.budget_management import views
from rest_framework import routers
from apps.budget_management.models import CustomUser, Family,Account,\
    Transaction

router = routers.DefaultRouter()
router.register('user', views.UserViewSet, basename=CustomUser)
router.register('family', views.FamilyViewSet, basename=Family)
router.register('account', views.AccountViewSet, basename=Account)
router.register('transaction', views.TransactionViewSet, basename=Transaction)

urlpatterns = [

    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),

]
