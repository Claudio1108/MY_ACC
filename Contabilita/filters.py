import django_filters
from .models import *

class ProtocolloFilter(django_filters.FilterSet):
    #cliente = django_filters.CharFilter(lookup_expr='icontains')
    #referente = django_filters.CharFilter(lookup_expr='icontains')
    #data = django_filters.NumberFilter(name='date_joined', lookup_expr='year')

    class Meta:
        model = Protocollo
        fields = {
            'cliente': ['exact', ],
            'referente': [ 'exact', ],
            'data': ['year', ],
        }