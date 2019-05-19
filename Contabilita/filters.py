import django_filters
from .models import *

class ProtocolloFilter(django_filters.FilterSet):

    class Meta:
        model = Protocollo
        fields = {
            'cliente': ['contains', ],
            'referente': ['contains', ],
            'indirizzo':['contains', ],
            'pratica': ['contains', ],
            'data': ['month','year'],
        }

class SpesaGestioneFilter(django_filters.FilterSet):

    class Meta:
        model = SpesaGestione
        fields = {
            'data': ['month','year' ],
            'fattura': ['contains', ],
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
            'fattura': ['contains', ],
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