from apps.budget_management.models import CustomUser
import django_filters
from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    #username = filters.CharFilter('username')
    #email = filters.CharFilter(method='filter_email')

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    # def filter_email(self, queryset, name, value):
    #     data = queryset.filter(email__icontains=value)
    #     print('@#@#@###@#', data)
    #     return data
