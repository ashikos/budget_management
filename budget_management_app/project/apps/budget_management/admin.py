from django.contrib import admin
from apps.budget_management import models

admin.site.register(models.CustomUser)
admin.site.register(models.Family)
admin.site.register(models.Account)


class AdminTransaction(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount']


admin.site.register(models.Transaction, AdminTransaction)
