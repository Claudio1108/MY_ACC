import django_filters
from .models import *


def print_query_param(value, key):
   if value and key:
       return "%s=%s&" % (key, value)

class ProtocolloFilter(django_filters.FilterSet):
    data_registrazione_year = django_filters.NumberFilter(label='Data Registrazione (Anno)', field_name='data_registrazione', lookup_expr='year')
    data_registrazione_month = django_filters.NumberFilter(label='Data Registrazione (Mese 1-12)', field_name='data_registrazione', lookup_expr='month')
    identificativo = django_filters.CharFilter(label='Identificativo', field_name='identificativo', lookup_expr='icontains')
    cliente = django_filters.CharFilter(label='Cliente', field_name='cliente', lookup_expr='icontains')
    referente = django_filters.CharFilter(label='Referente', field_name='referente', lookup_expr='icontains')
    indirizzo = django_filters.CharFilter(label='Indirizzo', field_name='indirizzo', lookup_expr='icontains')
    pratica = django_filters.CharFilter(label='Pratica', field_name='pratica', lookup_expr='icontains')
    data_consegna = django_filters.BooleanFilter(label='Data Consegna',field_name = 'data_consegna', lookup_expr='isnull', exclude=True)
    status = django_filters.RangeFilter(label='range (min-max)')

    # class Meta:
    #     model = Protocollo
    #     fields = ['identificativo','cliente','referente','indirizzo','pratica','data_consegna','status']

class SpesaGestioneFilter(django_filters.FilterSet):
    data_registrazione_year = django_filters.NumberFilter(label='Data Registrazione (Anno)', field_name='data_registrazione', lookup_expr='year')
    data_registrazione_month = django_filters.NumberFilter(label='Data Registrazione (Mese 1-12)', field_name='data_registrazione', lookup_expr='month')
    fattura = django_filters.CharFilter(label='Fattura', field_name='fattura', lookup_expr='icontains')
    causale = django_filters.CharFilter(label='Causale', field_name='causale', lookup_expr='icontains')

    # class Meta:
    #     model = SpesaGestione
    #     fields = ['fattura','causale']

class SpesaCommessaFilter(django_filters.FilterSet):
    data_registrazione_year = django_filters.NumberFilter(label='Data Registrazione (Anno)', field_name='data_registrazione', lookup_expr='year')
    data_registrazione_month = django_filters.NumberFilter(label='Data Registrazione (Mese 1-12)', field_name='data_registrazione', lookup_expr='month')
    #protocollo = django_filters.CharFilter(label='Protocollo', field_name='protocollo', lookup_expr='icontains')
    class Meta:
        model = SpesaCommessa
        fields = {
            'protocollo': ['exact', ],
        }

class RicavoFilter(django_filters.FilterSet):
    data_registrazione_year = django_filters.NumberFilter(label='Data Registrazione (Anno)', field_name='data_registrazione', lookup_expr='year')
    data_registrazione_month = django_filters.NumberFilter(label='Data Registrazione (Mese 1-12)', field_name='data_registrazione', lookup_expr='month')
    #protocollo = django_filters.CharFilter(label='Protocollo', field_name='protocollo', lookup_expr='icontains')

    class Meta:
        model = Ricavo
        fields = {
            'intestatario_fattura': ['exact', ],
            'protocollo': ['exact', ],
            'fattura': ['exact',]
        }

class GuadagnoEffettivoFilter(django_filters.FilterSet):
    data_registrazione_year = django_filters.NumberFilter(label='Data Registrazione (Anno)', field_name='data_registrazione', lookup_expr='year')
    data_registrazione_month = django_filters.NumberFilter(label='Data Registrazione (Mese 1-12)', field_name='data_registrazione', lookup_expr='month')

    # class Meta:
    #     model = GuadagnoEffettivo
    #     fields = []