import django_filters
from .models import *

def print_query_param(value, key):
   if value and key:
       return "%s=%s&" % (key, value)


class ProtocolloFilter(django_filters.FilterSet):
    #data_registrazione = django_filters.DateFilter(label='Data di Registrazione (gg/mm/aaaa)', field_name='data_registrazione', lookup_expr='exact')
    identificativo = django_filters.CharFilter(label='Identificativo', field_name='identificativo', lookup_expr='contains')
    cliente = django_filters.CharFilter(label='Cliente', field_name='cliente', lookup_expr='contains')
    referente = django_filters.CharFilter(label='Referente', field_name='referente', lookup_expr='contains')
    indirizzo = django_filters.CharFilter(label='Indirizzo', field_name='indirizzo', lookup_expr='contains')
    pratica = django_filters.CharFilter(label='Pratica', field_name='pratica', lookup_expr='contains')
    data_consegna = django_filters.BooleanFilter(label='Data Consegna',field_name = 'data_consegna', lookup_expr='isnull', exclude=True)
    status = django_filters.RangeFilter(label='range (min-max)')

    class Meta:
        model = Protocollo
        fields = ['identificativo','cliente','referente','indirizzo','pratica','data_consegna','status']

class SpesaGestioneFilter(django_filters.FilterSet):
    data = django_filters.DateFilter(label='Data di Registrazione (gg/mm/aaaa)', field_name='data', lookup_expr='exact')
    fattura = django_filters.CharFilter(label='Fattura', field_name='fattura', lookup_expr='exact')
    intestatario_fattura = django_filters.CharFilter(label='Intestatario Fattura', field_name='intestatario_fattura', lookup_expr='exact')
    causale = django_filters.CharFilter(label='Causale', field_name='causale', lookup_expr='contains')

    class Meta:
        model = SpesaGestione
        fields = ['data','fattura','intestatario_fattura','causale']

class SpesaCommessaFilter(django_filters.FilterSet):
    data = django_filters.DateFilter(label='Data di Registrazione (gg/mm/aaaa)', field_name='data', lookup_expr='exact')
    protocollo = django_filters.CharFilter(label='Protocollo', field_name='protocollo', lookup_expr='exact')
    class Meta:
        model = SpesaCommessa
        fields = ['data','protocollo']

class RicavoFilter(django_filters.FilterSet):
    data = django_filters.DateFilter(label='Data di Registrazione (gg/mm/aaaa)', field_name='data', lookup_expr='exact')
    fattura = django_filters.CharFilter(label='Fattura', field_name='fattura', lookup_expr='exact')
    intestatario_fattura = django_filters.CharFilter(label='Intestatario Fattura', field_name='intestatario_fattura',lookup_expr='exact')
    protocollo = django_filters.CharFilter(label='Protocollo', field_name='protocollo', lookup_expr='exact')


    class Meta:
        model = Ricavo
        fields = ['data','fattura','intestatario_fattura','protocollo']

class GuadagnoEffettivoFilter(django_filters.FilterSet):
    data = django_filters.DateFilter(label='Data di Registrazione (gg/mm/aaaa)', field_name='data', lookup_expr='exact')

    class Meta:
        model = GuadagnoEffettivo
        fields = ['data']