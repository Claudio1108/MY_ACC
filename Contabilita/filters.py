import django_filters
from .models import *

class ProtocolloFilter(django_filters.FilterSet):

    class Meta:
        model = Protocollo
        fields = {
            'cliente': ['contains', ],
            'referente': ['contains', ],
            'data': ['month','year'],
        }

class SpesaGestioneFilter(django_filters.FilterSet):

    class Meta:
        model = SpesaGestione
        fields = {
            'causale': ['contains', ],
            'data': ['month','year' ],
        }

class RicavoFilter(django_filters.FilterSet):

    class Meta:
        model = Ricavo
        fields = {
            'fattura': ['contains', ],
            'data': ['month','year' ],
        }