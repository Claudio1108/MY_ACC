import django_filters
from .models import *

class ClienteFilter(django_filters.FilterSet):
    nominativo = django_filters.CharFilter(label='Nominativo', field_name='nominativo', lookup_expr='icontains')

class ReferenteFilter(django_filters.FilterSet):
    nominativo = django_filters.CharFilter(label='Nominativo', field_name='nominativo', lookup_expr='icontains')

class ProtocolloFilter(django_filters.FilterSet):
    data_registrazione = django_filters.DateFromToRangeFilter(label='Data Registrazione (start-end) dd/mm/yyyy')
    identificativo = django_filters.CharFilter(label='Identificativo', field_name='identificativo', lookup_expr='icontains')
    cliente = django_filters.CharFilter(label='Cliente', field_name='cliente', lookup_expr='icontains')
    referente = django_filters.CharFilter(label='Referente', field_name='referente', lookup_expr='icontains')
    indirizzo = django_filters.CharFilter(label='Indirizzo', field_name='indirizzo', lookup_expr='icontains')
    pratica = django_filters.CharFilter(label='Pratica', field_name='pratica', lookup_expr='icontains')
    data_consegna = django_filters.BooleanFilter(label='Data Consegna',field_name = 'data_consegna', lookup_expr='isnull', exclude=True)
    status = django_filters.RangeFilter(label='Stato Protocollo (min-max) gg ', field_name = 'status')

    class Meta:
        model = Protocollo
        fields = {
            'responsabile': ['exact'],
        }

class ConsulenzaFilter(django_filters.FilterSet):
    data_registrazione = django_filters.DateFromToRangeFilter(label='Data Registrazione (start-end) dd/mm/yyyy')
    cliente = django_filters.CharFilter(label='Cliente', field_name='cliente', lookup_expr='icontains')
    indirizzo = django_filters.CharFilter(label='Indirizzo', field_name='indirizzo', lookup_expr='icontains')
    attivita = django_filters.CharFilter(label='Attività', field_name='attivita', lookup_expr='icontains')
    data_consegna = django_filters.BooleanFilter(label='Data Consegna',field_name = 'data_consegna', lookup_expr='isnull', exclude=True)
    status = django_filters.RangeFilter(label='Stato Consulenza (min-max) gg ', field_name = 'status')

    class Meta:
        model = Consulenza
        fields = {
            'responsabile': ['exact'],
        }

class SpesaGestioneFilter(django_filters.FilterSet):
    data_registrazione = django_filters.DateFromToRangeFilter(label='Data Registrazione (start-end) dd/mm/yyyy')
    fattura = django_filters.CharFilter(label='Fattura', field_name='fattura', lookup_expr='icontains')
    causale = django_filters.CharFilter(label='Causale', field_name='causale', lookup_expr='icontains')
    importo = django_filters.RangeFilter(label='Importo (min-max) €', field_name='importo')

    class Meta:
        model = SpesaGestione
        fields = {
            'provenienza': ['exact'],
        }

class SpesaCommessaFilter(django_filters.FilterSet):
    data_registrazione = django_filters.DateFromToRangeFilter(label='Data Registrazione (start-end) dd/mm/yyyy')
    protocollo_exist = django_filters.BooleanFilter(label='Esistenza Protocollo', field_name='protocollo', lookup_expr='isnull', exclude=True)
    protocollo_id = django_filters.CharFilter(label='Protocollo (id)', field_name='protocollo__identificativo', lookup_expr='icontains')
    protocollo_address = django_filters.CharFilter(label='Protocollo (indirizzo)', field_name='protocollo__indirizzo', lookup_expr='icontains')
    importo = django_filters.RangeFilter(label='Importo (min-max) €', field_name='importo')

    class Meta:
        model = SpesaCommessa
        fields = {
            'provenienza': ['exact'],
        }

class RicavoFilter(django_filters.FilterSet):
    data_registrazione = django_filters.DateFromToRangeFilter(label='Data Registrazione (start-end) dd/mm/yyyy')
    protocollo_exist = django_filters.BooleanFilter(label='Esistenza Protocollo', field_name='protocollo', lookup_expr='isnull', exclude=True)
    protocollo_id = django_filters.CharFilter(label='Protocollo (id)', field_name='protocollo__identificativo', lookup_expr='icontains')
    protocollo_address = django_filters.CharFilter(label='Protocollo (indirizzo)', field_name='protocollo__indirizzo', lookup_expr='icontains')
    importo = django_filters.RangeFilter(label='Importo (min-max) €', field_name='importo')

    class Meta:
        model = Ricavo
        fields = {
            'intestatario_fattura': ['exact'],
            'fattura': ['exact'],
            'destinazione': ['exact'],
        }

class GuadagnoEffettivoFilter(django_filters.FilterSet):
    data_registrazione = django_filters.DateFromToRangeFilter(label='Data Registrazione (start-end) dd/mm/yyyy')
    importo = django_filters.RangeFilter(label='Importo (min-max) €', field_name='importo')

    class Meta:
        model = GuadagnoEffettivo
        fields = {
            'provenienza': ['exact'],
        }