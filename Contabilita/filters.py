import django_filters
from .models import *


class MyRangeWidget(django_filters.widgets.RangeWidget):

    def __init__(self, from_attrs=None, to_attrs=None, attrs=None):
        super(MyRangeWidget, self).__init__(attrs)
        if from_attrs:
            self.widgets[0].attrs.update(from_attrs)
        if to_attrs:
            self.widgets[1].attrs.update(to_attrs)

class ClienteFilter(django_filters.FilterSet):
    nominativo = django_filters.CharFilter(label='Nominativo', field_name='nominativo', lookup_expr='icontains')

class ReferenteFilter(django_filters.FilterSet):
    nominativo = django_filters.CharFilter(label='Nominativo', field_name='nominativo', lookup_expr='icontains')

class ProtocolloFilter(django_filters.FilterSet):
    data_registrazione = django_filters.DateFromToRangeFilter(label='Data Registrazione', widget=MyRangeWidget(
        from_attrs={'placeholder':'start (dd/mm/yyyy)'},
        to_attrs={'placeholder':'end (dd/mm/yyyy)'},
    ))
    identificativo = django_filters.CharFilter(label='Identificativo', field_name='identificativo', lookup_expr='icontains')
    cliente = django_filters.CharFilter(label='Cliente', field_name='cliente__nominativo', lookup_expr='icontains')
    referente = django_filters.CharFilter(label='Referente', field_name='referente__nominativo', lookup_expr='icontains')
    indirizzo = django_filters.CharFilter(label='Indirizzo', field_name='indirizzo', lookup_expr='icontains')
    pratica = django_filters.CharFilter(label='Pratica', field_name='pratica', lookup_expr='icontains')
    data_consegna = django_filters.BooleanFilter(label='Data Consegna',field_name = 'data_consegna', lookup_expr='isnull', exclude=True)
    status = django_filters.RangeFilter(label='Stato Protocollo', field_name = 'status', widget=MyRangeWidget(
        from_attrs={'placeholder':'min'},
        to_attrs={'placeholder':'max'},
    ))

    class Meta:
        model = Protocollo
        fields = {
            'responsabile': ['exact'],
        }

class ConsulenzaFilter(django_filters.FilterSet):
    data_registrazione = django_filters.DateFromToRangeFilter(label='Data Registrazione', widget=MyRangeWidget(
        from_attrs={'placeholder': 'start (dd/mm/yyyy)'},
        to_attrs={'placeholder': 'end (dd/mm/yyyy)'},
    ))
    richiedente = django_filters.CharFilter(label='Richiedente', field_name='richiedente', lookup_expr='icontains')
    indirizzo = django_filters.CharFilter(label='Indirizzo', field_name='indirizzo', lookup_expr='icontains')
    attivita = django_filters.CharFilter(label='Attività', field_name='attivita', lookup_expr='icontains')
    data_consegna = django_filters.BooleanFilter(label='Data Consegna',field_name = 'data_consegna', lookup_expr='isnull', exclude=True)
    status = django_filters.RangeFilter(label='Stato Protocollo', field_name='status', widget=MyRangeWidget(
        from_attrs={'placeholder': 'min'},
        to_attrs={'placeholder': 'max'},
    ))

    class Meta:
        model = Consulenza
        fields = {
            'responsabile': ['exact'],
        }

class SpesaGestioneFilter(django_filters.FilterSet):
    data_registrazione = django_filters.DateFromToRangeFilter(label='Data Registrazione', widget=MyRangeWidget(
        from_attrs={'placeholder': 'start (dd/mm/yyyy)'},
        to_attrs={'placeholder': 'end (dd/mm/yyyy)'},
    ))
    fattura = django_filters.CharFilter(label='Fattura', field_name='fattura', lookup_expr='icontains')
    causale = django_filters.CharFilter(label='Causale', field_name='causale', lookup_expr='icontains')
    importo = django_filters.RangeFilter(label='Importo (€)', field_name='importo', widget=MyRangeWidget(
        from_attrs={'placeholder': 'min'},
        to_attrs={'placeholder': 'max'},
    ))

    class Meta:
        model = SpesaGestione
        fields = {
            'provenienza': ['exact'],
        }

class SpesaCommessaFilter(django_filters.FilterSet):
    data_registrazione = django_filters.DateFromToRangeFilter(label='Data Registrazione', widget=MyRangeWidget(
        from_attrs={'placeholder': 'start (dd/mm/yyyy)'},
        to_attrs={'placeholder': 'end (dd/mm/yyyy)'},
    ))
    protocollo_exist = django_filters.BooleanFilter(label='Esistenza Protocollo', field_name='protocollo', lookup_expr='isnull', exclude=True)
    protocollo_id = django_filters.CharFilter(label='Protocollo (id)', field_name='protocollo__identificativo', lookup_expr='icontains')
    protocollo_address = django_filters.CharFilter(label='Protocollo (indirizzo)', field_name='protocollo__indirizzo', lookup_expr='icontains')
    importo = django_filters.RangeFilter(label='Importo (€)', field_name='importo', widget=MyRangeWidget(
        from_attrs={'placeholder': 'min'},
        to_attrs={'placeholder': 'max'},
    ))

    class Meta:
        model = SpesaCommessa
        fields = {
            'provenienza': ['exact'],
        }

class RicavoFilter(django_filters.FilterSet):
    data_registrazione = django_filters.DateFromToRangeFilter(label='Data Registrazione', widget=MyRangeWidget(
        from_attrs={'placeholder': 'start (dd/mm/yyyy)'},
        to_attrs={'placeholder': 'end (dd/mm/yyyy)'},
    ))
    protocollo_exist = django_filters.BooleanFilter(label='Esistenza Protocollo', field_name='protocollo', lookup_expr='isnull', exclude=True)
    protocollo_id = django_filters.CharFilter(label='Protocollo (id)', field_name='protocollo__identificativo', lookup_expr='icontains')
    protocollo_address = django_filters.CharFilter(label='Protocollo (indirizzo)', field_name='protocollo__indirizzo', lookup_expr='icontains')
    importo = django_filters.RangeFilter(label='Importo (€)', field_name='importo', widget=MyRangeWidget(
        from_attrs={'placeholder': 'min'},
        to_attrs={'placeholder': 'max'},
    ))

    class Meta:
        model = Ricavo
        fields = {
            'intestatario_fattura': ['exact'],
            'fattura': ['exact'],
            'destinazione': ['exact'],
        }

class GuadagnoEffettivoFilter(django_filters.FilterSet):
    data_registrazione = django_filters.DateFromToRangeFilter(label='Data Registrazione', widget=MyRangeWidget(
        from_attrs={'placeholder': 'start (dd/mm/yyyy)'},
        to_attrs={'placeholder': 'end (dd/mm/yyyy)'},
    ))
    importo = django_filters.RangeFilter(label='Importo (min-max) €', field_name='importo')

    class Meta:
        model = GuadagnoEffettivo
        fields = {
            'provenienza': ['exact'],
        }