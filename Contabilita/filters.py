import django_filters
from .models import *

class ProtocolloFilter(django_filters.FilterSet):

    class Meta:
        model = Protocollo
        fields = {
            'cliente': ['exact', ],
            'referente': [ 'exact', ],
            'data': ['month','year' ],
        }

class SpesaGestioneFilter(django_filters.FilterSet):

    class Meta:
        model = SpesaGestione
        fields = {
            'causale': ['exact', ],
            'data': ['month','year' ],
        }