import django_filters
from .models import *


def print_query_param(value, key):
   if value and key:
       return "%s=%s&" % (key, value)

class ProtocolloFilter(django_filters.FilterSet):

    class Meta:
        model = Protocollo
        fields = {
            'identificativo': ['contains', ],
            'cliente': ['contains', ],
            'indirizzo':['contains', ],
            'pratica': ['contains', ],
            'referente': ['contains', ],
            'data': ['month','year'],
        }

class SpesaGestioneFilter(django_filters.FilterSet):

    class Meta:
        model = SpesaGestione
        fields = {
            'data': ['month','year' ],
            'fattura': ['exact',  ],
            'intestatario_fattura': ['exact', ],
            'causale': ['contains', ],
        }

class SpesaCommessaFilter(django_filters.FilterSet):

    class Meta:
        model = SpesaCommessa
        fields = {
            'data': ['month','year' ],
            'protocollo': ['exact', ],
        }

class RicavoFilter(django_filters.FilterSet):

    class Meta:
        model = Ricavo
        fields = {
            'fattura': ['exact',  ],
            'intestatario_fattura': ['exact', ],
            'protocollo': ['exact', ],
            'data': ['month','year' ],
        }

class GuadagnoEffettivoFilter(django_filters.FilterSet):

    class Meta:
        model = GuadagnoEffettivo
        fields = {
            'data': ['month','year' ],
        }