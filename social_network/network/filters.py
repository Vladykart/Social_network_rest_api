from django_filters import rest_framework as filters
from .models import PostLike


class LikeDateFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name="created", lookup_expr='gte')
    date_to = filters.DateFilter(field_name="created", lookup_expr='lte')
    class Meta:
        model = PostLike

        fields = ['liked_date', 'value']
