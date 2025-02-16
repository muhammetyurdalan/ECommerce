import django_filters
import products.models as models


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = models.Product
        fields = {
            'name': ['icontains'],
            'price': ['lt', 'gt'],
            'score': ['lt', 'gt'],
            'category__name': ['exact'],
            'variations__variation_option__value': ['exact'],
            'variations__variation_option__variation__name': ['exact'],
        }