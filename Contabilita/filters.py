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
    status = django_filters.RangeFilter(label='Stato Protocollo (min-max)gg ', field_name = 'status')

class SpesaGestioneFilter(django_filters.FilterSet):
    data_registrazione_year = django_filters.NumberFilter(label='Data Registrazione (Anno)', field_name='data_registrazione', lookup_expr='year')
    data_registrazione_month = django_filters.NumberFilter(label='Data Registrazione (Mese 1-12)', field_name='data_registrazione', lookup_expr='month')
    fattura = django_filters.CharFilter(label='Fattura', field_name='fattura', lookup_expr='icontains')
    causale = django_filters.CharFilter(label='Causale', field_name='causale', lookup_expr='icontains')
    importo = django_filters.RangeFilter(label='Importo (min-max)€', field_name='importo')

class SpesaCommessaFilter(django_filters.FilterSet):
    data_registrazione_year = django_filters.NumberFilter(label='Data Registrazione (Anno)', field_name='data_registrazione', lookup_expr='year')
    data_registrazione_month = django_filters.NumberFilter(label='Data Registrazione (Mese 1-12)', field_name='data_registrazione', lookup_expr='month')
    protocollo_exist = django_filters.BooleanFilter(label='Esistenza Protocollo', field_name='protocollo', lookup_expr='isnull', exclude=True)
    protocollo_id = django_filters.CharFilter(label='Protocollo (id)', field_name='protocollo__identificativo', lookup_expr='icontains')
    protocollo_address = django_filters.CharFilter(label='Protocollo (indirizzo)', field_name='protocollo__indirizzo', lookup_expr='icontains')
    importo = django_filters.RangeFilter(label='Importo (min-max)€', field_name='importo')

class RicavoFilter(django_filters.FilterSet):
    data_registrazione_year = django_filters.NumberFilter(label='Data Registrazione (Anno)', field_name='data_registrazione', lookup_expr='year')
    data_registrazione_month = django_filters.NumberFilter(label='Data Registrazione (Mese 1-12)', field_name='data_registrazione', lookup_expr='month')
    protocollo_exist = django_filters.BooleanFilter(label='Esistenza Protocollo', field_name='protocollo', lookup_expr='isnull', exclude=True)
    protocollo_id = django_filters.CharFilter(label='Protocollo (id)', field_name='protocollo__identificativo', lookup_expr='icontains')
    protocollo_address = django_filters.CharFilter(label='Protocollo (indirizzo)', field_name='protocollo__indirizzo', lookup_expr='icontains')
    importo = django_filters.RangeFilter(label='Importo (min-max)€', field_name='importo')

    class Meta:
        model = Ricavo
        fields = {
            'intestatario_fattura': ['exact'],
            'fattura': ['exact']
        }

class GuadagnoEffettivoFilter(django_filters.FilterSet):
    data_registrazione_year = django_filters.NumberFilter(label='Data Registrazione (Anno)', field_name='data_registrazione', lookup_expr='year')
    data_registrazione_month = django_filters.NumberFilter(label='Data Registrazione (Mese 1-12)', field_name='data_registrazione', lookup_expr='month')
    importo = django_filters.RangeFilter(label='Importo (min-max)€', field_name='importo')
