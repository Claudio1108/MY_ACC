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
    nominativo = django_filters.CharFilter(label='Nominativo', field_name='nominativo', lookup_expr='istartswith')

class ReferenteFilter(django_filters.FilterSet):
    nominativo = django_filters.CharFilter(label='Nominativo', field_name='nominativo', lookup_expr='istartswith')

class ProtocolloFilter(django_filters.FilterSet):
    data_registrazione = django_filters.DateFromToRangeFilter(label='Data Registrazione', widget=MyRangeWidget(
        from_attrs={'placeholder':'inizio (dd/mm/yyyy)'},
        to_attrs={'placeholder':'fine (dd/mm/yyyy)'},
    ))
    stato_protocollo = django_filters.ChoiceFilter(
        label='Stato Protocollo',
        choices=(('scaduti', 'Scaduti 🔴'), ('in_scadenza', 'In Scadenza 🟠'), ('puntuale', 'Puntuale 🟢'), ('consegnato', 'Consegnato ⚫'), ('attivo', 'Attivo ⚙️')),
        method='filter_by_stato_protocollo',
        empty_label='Non Specificato'
    )
    identificativo = django_filters.CharFilter(label='Identificativo', field_name='identificativo', lookup_expr='istartswith')
    cliente = django_filters.CharFilter(label='Cliente', field_name='cliente__nominativo', lookup_expr='istartswith')
    referente = django_filters.CharFilter(label='Referente', field_name='referente__nominativo', lookup_expr='istartswith')
    indirizzo = django_filters.CharFilter(label='Indirizzo', field_name='indirizzo', lookup_expr='istartswith')
    pratica = django_filters.CharFilter(label='Pratica', field_name='pratica', lookup_expr='istartswith')

    def filter_by_stato_protocollo(self, queryset, name, value):
        if value == 'scaduti':
            return queryset.filter(status__lte=-1)
        elif value == 'in_scadenza':
            return queryset.filter(status__gte=0, status__lte=3)
        elif value == 'puntuale':
            return queryset.filter(status__gte=4)
        elif value == 'consegnato':
            return queryset.filter(data_consegna__isnull=False)
        elif value == 'attivo':
            return queryset.filter(data_consegna__isnull=True)
        return queryset

class ConsulenzaFilter(django_filters.FilterSet):
    data_registrazione = django_filters.DateFromToRangeFilter(label='Data Registrazione', widget=MyRangeWidget(
        from_attrs={'placeholder': 'inizio (dd/mm/yyyy)'},
        to_attrs={'placeholder': 'fine (dd/mm/yyyy)'},
    ))
    stato_consulenza = django_filters.ChoiceFilter(
        label='Stato Consulenza',
        choices=(('scaduti', 'Scaduti 🔴'), ('in_scadenza', 'In Scadenza 🟠'), ('puntuale', 'Puntuale 🟢'), ('consegnato', 'Consegnato ⚫'), ('attivo', 'Attivo ⚙️')),
        method='filter_by_stato_consulenza',
        empty_label='Non Specificato'
    )
    richiedente = django_filters.CharFilter(label='Richiedente', field_name='richiedente', lookup_expr='istartswith')
    indirizzo = django_filters.CharFilter(label='Indirizzo', field_name='indirizzo', lookup_expr='istartswith')
    attivita = django_filters.CharFilter(label='Attività', field_name='attivita', lookup_expr='istartswith')

    def filter_by_stato_consulenza(self, queryset, name, value):
        if value == 'scaduti':
            return queryset.filter(status__lte=-1)
        elif value == 'in_scadenza':
            return queryset.filter(status__gte=0, status__lte=3)
        elif value == 'puntuale':
            return queryset.filter(status__gte=4)
        elif value == 'consegnato':
            return queryset.filter(data_consegna__isnull=False)
        elif value == 'attivo':
            return queryset.filter(data_consegna__isnull=True)
        return queryset

class SpesaGestioneFilter(django_filters.FilterSet):
    data_registrazione = django_filters.DateFromToRangeFilter(label='Data Registrazione', widget=MyRangeWidget(
        from_attrs={'placeholder': 'inizio (dd/mm/yyyy)'},
        to_attrs={'placeholder': 'fine (dd/mm/yyyy)'},
    ))
    importo = django_filters.RangeFilter(label='Importo (€) ', field_name='importo', widget=MyRangeWidget(
        from_attrs={'placeholder': 'min'},
        to_attrs={'placeholder': 'max'},
    ))
    fattura = django_filters.CharFilter(label='Fattura', field_name='fattura', lookup_expr='istartswith')
    causale = django_filters.CharFilter(label='Causale', field_name='causale', lookup_expr='istartswith')
    provenienza = django_filters.ChoiceFilter(
        label='Provenienza',
        field_name='provenienza',
        choices=SpesaGestione._meta.get_field('provenienza').choices  # oppure specifica tu le choices
    )

    class Meta:
        model = SpesaGestione
        fields = []


class SpesaCommessaFilter(django_filters.FilterSet):
    data_registrazione = django_filters.DateFromToRangeFilter(label='Data Registrazione', widget=MyRangeWidget(
        from_attrs={'placeholder': 'inizio (dd/mm/yyyy)'},
        to_attrs={'placeholder': 'fine (dd/mm/yyyy)'},
    ))
    importo = django_filters.RangeFilter(label='Importo (€) ', field_name='importo', widget=MyRangeWidget(
        from_attrs={'placeholder': 'min'},
        to_attrs={'placeholder': 'max'},
    ))
    protocollo_id = django_filters.CharFilter(label='Protocollo [Identificativo]', field_name='protocollo__identificativo', lookup_expr='istartswith')
    protocollo_address = django_filters.CharFilter(label='Protocollo [Indirizzo]', field_name='protocollo__indirizzo', lookup_expr='istartswith')
    provenienza = django_filters.ChoiceFilter(
        label='Provenienza',
        field_name='provenienza',
        choices=SpesaCommessa._meta.get_field('provenienza').choices  # oppure specifica tu le choices
    )

    class Meta:
        model = SpesaCommessa
        fields = []

class RicavoFilter(django_filters.FilterSet):
    data_registrazione = django_filters.DateFromToRangeFilter(label='Data Registrazione', widget=MyRangeWidget(
        from_attrs={'placeholder': 'inizio (dd/mm/yyyy)'},
        to_attrs={'placeholder': 'fine (dd/mm/yyyy)'},
    ))
    importo = django_filters.RangeFilter(label='Importo (€) ', field_name='importo', widget=MyRangeWidget(
        from_attrs={'placeholder': 'min'},
        to_attrs={'placeholder': 'max'},
    ))
    protocollo_exist = django_filters.BooleanFilter(label='Esistenza Protocollo', field_name='protocollo', lookup_expr='isnull', exclude=True)
    protocollo_id = django_filters.CharFilter(label='Protocollo [Identificativo]', field_name='protocollo__identificativo', lookup_expr='istartswith')
    protocollo_address = django_filters.CharFilter(label='Protocollo [Indirizzo]', field_name='protocollo__indirizzo', lookup_expr='istartswith')
    fattura = django_filters.ChoiceFilter(
        label='Fattura',
        field_name='fattura',
        choices=Ricavo._meta.get_field('fattura').choices  # oppure specifica tu le choices
    )
    destinazione = django_filters.ChoiceFilter(
        label='Destinazione',
        field_name='destinazione',
        choices=Ricavo._meta.get_field('destinazione').choices  # oppure specifica tu le choices
    )

    class Meta:
        model = Ricavo
        fields = []
