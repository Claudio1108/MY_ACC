import re
import calendar
from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from .models import *
from dal import autocomplete
from Contabilita import sqlite_queries as sqlite
from django.forms import TextInput
from django.db.models import Sum
from decimal import Decimal, ROUND_HALF_UP

YEARS = [x for x in range(1970, 2050)]
MESI_ITALIANI = [
    (1, "Gennaio"), (2, "Febbraio"), (3, "Marzo"),
    (4, "Aprile"), (5, "Maggio"), (6, "Giugno"),
    (7, "Luglio"), (8, "Agosto"), (9, "Settembre"),
    (10, "Ottobre"), (11, "Novembre"), (12, "Dicembre")
]

class DateInput(forms.DateInput):
    input_type = 'date'

class DateInput2(forms.DateInput):
    input_type = 'date'

    def __init__(self, **kwargs):
        kwargs['format'] = '%Y-%m-%d'  # formato HTML5
        super().__init__(**kwargs)

class formCliente(forms.ModelForm):
    class Meta:
        model = RubricaClienti
        fields = "__all__"
        labels = {
            "nominativo": "Cognome - Nome* ",
            "tel": "Telefono* ",
            "mail": "Mail ",
            "note": "Note "
        }

class formReferente(forms.ModelForm):
    class Meta:
        model = RubricaReferenti
        fields = "__all__"
        labels = {
            "nominativo": "Azienda - Cognome - Nome* ",
            "tel": "Telefono* ",
            "mail": "Mail ",
            "note": "Note "
        }

class formProtocol(forms.ModelForm):
    class Meta:
        model = Protocollo
        fields = "__all__"
        labels = {
            "cliente": "Cliente* ",
            "indirizzo": "Indirizzo* ",
            "parcella": "Parcella* ",
            "pratica": "Pratica* ",
            "note": "Note ",
            "data_registrazione": "Data Registrazione* ",
            "data_scadenza": "Data Scadenza* ",
            "data_consegna": "Data Consegna "
        }
        widgets = {
            'data_registrazione': DateInput(attrs={'required': 'required'}),
            'data_scadenza': DateInput(attrs={'required': 'required'}),
            'data_consegna': DateInput(attrs={}),
            'cliente': autocomplete.ModelSelect2(url='cliente_autocomp', attrs={'required': 'required'}),
            'indirizzo': TextInput(attrs={'required': 'required'}),
            'parcella': TextInput(attrs={'required': 'required'}),
            'pratica': TextInput(attrs={'required': 'required'}),
            'referente': autocomplete.ModelSelect2(url='referente_autocomp', attrs={}),
        }

    def check_date(self):
        data = self.data.copy()
        return data['data_scadenza'] >= data['data_registrazione'] and (
            data['data_consegna'] >= data['data_registrazione'] if data['data_consegna'] else True)

    def set_identificativo(self,value):
        data = self.data.copy()
        data['identificativo'] = value
        self.data = data

    def set_status(self,value):
        data = self.data.copy()
        data['status'] = value
        self.data = data

class formProtocolUpdate(forms.ModelForm):
    class Meta:
        model = Protocollo
        fields = "__all__"
        exclude = []
        labels = {
            "cliente": "Cliente* ",
            "referente": "Referente ",
            "indirizzo": "Indirizzo* ",
            "parcella": "Parcella* ",
            "pratica": "Pratica* ",
            "note": "Note ",
            "data_registrazione": "Data Registrazione* ",
            "data_scadenza": "Data Scadenza* ",
            "data_consegna": "Data Consegna "
        }
        widgets = {
            'data_registrazione': DateInput2(format='%Y-%m-%d'),
            'data_scadenza': DateInput2(format='%Y-%m-%d'),
            'data_consegna': DateInput2(format='%Y-%m-%d'),
            'cliente': autocomplete.ModelSelect2(url='cliente_autocomp'),
            'referente': autocomplete.ModelSelect2(url='referente_autocomp')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['identificativo'].disabled = True

    def check_date(self):
        data = self.data.copy()
        return data['data_scadenza'] >= data['data_registrazione'] and (
            data['data_consegna'] >= data['data_registrazione'] if data['data_consegna'] else True)

    def check_ricavi_on_protocollo(self, id_protocollo, parcella):
        somma_importi_ricavi = Ricavo.objects.filter(protocollo=id_protocollo).aggregate(Sum('importo'))['importo__sum'] or 0
        return somma_importi_ricavi <= Decimal(parcella)

    def set_identificativo(self,value):
        data = self.data.copy()
        data['identificativo'] = value
        self.data = data

    def set_status(self, value):
        data = self.data.copy()
        data['status'] = value
        self.data = data

class formConsulenza(forms.ModelForm):
    class Meta:
        model = Consulenza
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "richiedente": "Richiedente ",
            "indirizzo": "Indirizzo* ",
            "attivita": "Attività* ",
            "compenso": "Compenso* ",
            "note": "Note ",
            "data_scadenza": "Data Scadenza* ",
            "data_consegna": "Data Consegna "
        }
        widgets = {
            'data_registrazione': DateInput(),
            'data_scadenza': DateInput(),
            'data_consegna': DateInput(),
            'status' : forms.HiddenInput()
        }

    def check_date(self):
        data = self.data.copy()
        return data['data_scadenza'] >= data['data_registrazione'] and (
            data['data_consegna'] >= data['data_registrazione'] if data['data_consegna'] else True)

    def set_status(self,value):
        data = self.data.copy()
        data['status'] = value
        self.data = data

class formConsulenzaUpdate(forms.ModelForm):
    class Meta:
        model = Consulenza
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "richiedente": "Richiedente ",
            "indirizzo": "Indirizzo* ",
            "attivita": "Attività* ",
            "compenso": "Compenso* ",
            "note": "Note ",
            "data_scadenza": "Data Scadenza* ",
            "data_consegna": "Data Consegna "
        }
        widgets = {
            'data_registrazione': DateInput2(format='%Y-%m-%d'),
            'data_scadenza': DateInput2(format='%Y-%m-%d'),
            'data_consegna': DateInput2(format='%Y-%m-%d'),
            'status': forms.HiddenInput()
        }

    def check_date(self):
        data = self.data.copy()
        return data['data_scadenza'] >= data['data_registrazione'] and (
            data['data_consegna'] >= data['data_registrazione'] if data['data_consegna'] else True)

    def set_status(self, value):
        data = self.data.copy()
        data['status'] = value
        self.data = data

class formFattura(forms.ModelForm):
    class Meta:
        model = Fattura
        fields = ('data_registrazione', 'imponibile', 'protocollo', 'identificativo', 'importo', 'intestatario')
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "imponibile": "Imponibile* ",
            "protocollo": "Protocollo ",
            "intestatario": "Intestatario "
        }
        widgets = {
            'data_registrazione': DateInput(),
            'protocollo': autocomplete.ModelSelect2(url='proto_autocomp'),
            'intestatario': autocomplete.ListSelect2(url='cliente_referente_autocomp')
        }

    def set_identificativo(self, value):
        data = self.data.copy()
        data['identificativo'] = value
        self.data = data

    def calcola_importo(self, imponibile):
        data = self.data.copy()
        data['importo'] = (Decimal(str(imponibile)) * Decimal('1.04')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.data = data

class formFatturaUpdate(forms.ModelForm):
    intestatario = forms.CharField(
        widget=autocomplete.ListSelect2(url='cliente_referente_autocomp'),
        required=False
    )
    class Meta:
        model = Fattura
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "imponibile": "Imponibile* ",
            "protocollo": "Protocollo ",
            "intestatario": "Intestatario "
        }
        widgets = {
            'data_registrazione': DateInput2(format='%Y-%m-%d'),
            'protocollo': autocomplete.ModelSelect2(url='proto_autocomp'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['identificativo'].disabled = True
        # se c'è un valore salvato in intestatario, aggiungilo tra le opzioni di Select2
        initial_intestatario = self.initial.get('intestatario') or self.instance.intestatario
        if initial_intestatario:
            self.fields['intestatario'].widget.choices = [(initial_intestatario, initial_intestatario)]

    def set_identificativo(self, value):
        data = self.data.copy()
        data['identificativo'] = value
        self.data = data

    def calcola_importo(self, imponibile):
        data = self.data.copy()
        data['importo'] = (Decimal(str(imponibile)) * Decimal('1.04')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.data = data

class formRicavo(forms.ModelForm):
    class Meta:
        model = Ricavo
        fields = ('data_registrazione','movimento','importo','fattura', 'protocollo', 'note', 'destinazione')
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "movimento": "Movimento ",
            "importo": "Importo* ",
            "fattura": "Fattura ",
            "protocollo": "Protocollo ",
            "note": "Note ",
            "destinazione": "Destinazione "
        }
        widgets = {
            'data_registrazione': DateInput(),
            'protocollo': autocomplete.ModelSelect2(url='proto_autocomp'),
            'fattura': autocomplete.ModelSelect2(url='fattura_autocomp')
        }

    def Check1(self):
        id_protocollo = self.data['protocollo']
        protocollo = Protocollo.objects.get(id=id_protocollo)
        return sqlite.extract_sum_all_importi_ricavi_of_protocol(str(id_protocollo)) + float(self.data['importo']) <= protocollo.parcella

class formRicavoUpdate(forms.ModelForm):
    class Meta:
        model = Ricavo
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "movimento": "Movimento ",
            "importo": "Importo* ",
            "fattura": "Fattura ",
            "intestatario_fattura": "Intestatario Fattura ",
            "protocollo": "Protocollo ",
            "note": "Note ",
            "destinazione": "Destinazione "
        }
        widgets = {
            'data_registrazione': DateInput2(format='%Y-%m-%d'),
            'protocollo': autocomplete.ModelSelect2(url='proto_autocomp'),
            'fattura': autocomplete.ModelSelect2(url='fattura_autocomp')
        }

    def Check2(self, id_ricavo):
        id_protocollo = self.data['protocollo']
        protocollo = Protocollo.objects.get(id=id_protocollo)
        return sqlite.extract_sum_importi_ricavi_of_protocol_excluding_specific_ricavo(str(id_protocollo),
                re.findall("(\d+)", str(id_ricavo))[0]) + float(self.data['importo']) <= protocollo.parcella

class formSpesaCommessa(forms.ModelForm):
    class Meta:
        model = SpesaCommessa
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "importo": "Importo* ",
            "protocollo": "Protocollo ",
            "note": "Note ",
            "provenienza": "Provenienza "
        }
        widgets = {
            'data_registrazione': DateInput(),
            'protocollo': autocomplete.ModelSelect2(url='proto_autocomp')
        }

class formSpesaCommessaUpdate(forms.ModelForm):
    class Meta:
        model = SpesaCommessa
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "importo": "Importo* ",
            "protocollo": "Protocollo ",
            "note": "Note ",
            "provenienza": "Provenienza "
        }
        widgets = {
            'data_registrazione': DateInput2(format='%Y-%m-%d'),
            'protocollo': autocomplete.ModelSelect2(url='proto_autocomp')
        }

class formSpesaGestione(forms.ModelForm):
    class Meta:
        model = SpesaGestione
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "importo": "Importo* ",
            "causale": "Causale ",
            "f24": "F24 ",
            "fattura": "Fattura ",
            "provenienza": "Provenienza "
        }
        widgets = {'data_registrazione': DateInput(),
                   'f24': autocomplete.ModelSelect2(url='f24_autocomp')
        }

class formSpesaGestioneUpdate(forms.ModelForm):
    class Meta:
        model = SpesaGestione
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "importo": "Importo* ",
            "causale": "Causale ",
            "f24": "F24 ",
            "fattura": "Fattura ",
            "provenienza": "Provenienza "
        }
        widgets = {'data_registrazione': DateInput2(format='%Y-%m-%d'),
                   'f24': autocomplete.ModelSelect2(url='f24_autocomp')
        }


class formCodiceTributo(forms.ModelForm):
    class Meta:
        model = CodiceTributo
        fields = "__all__"
        labels = {
            "f24": "F24 ",
            "identificativo": "Identificativo* ",
            "anno": "Anno* ",
            "mese": "Mese ",
            "credito": "Credito ",
            "debito": "Debito "
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['f24'].required = False
        self.fields['f24'].widget.attrs['disabled'] = 'disabled'

class formCodiceTributoUpdate(forms.ModelForm):
    class Meta:
        model = CodiceTributo
        fields = "__all__"
        labels = {
            "f24": "F24 ",
            "identificativo": "Identificativo* ",
            "anno": "Anno ",
            "mese": "Mese ",
            "credito": "Credito ",
            "debito": "Debito ",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['identificativo'].widget.attrs['disabled'] = 'disabled'
        self.fields['f24'].required = False
        self.fields['f24'].widget.attrs['disabled'] = 'disabled'

class formF24(forms.ModelForm):
    class Meta:
        model = F24
        fields = "__all__"
        labels = {
            "identificativo": "Identificativo* ",
            "data_scadenza": "Data Scadenza* ",
            "ente": "Ente* ",
        }
        widgets = {
            'data_scadenza': DateInput2(format='%Y-%m-%d')
        }

class formF24Update(forms.ModelForm):
    class Meta:
        model = F24
        fields = "__all__"
        labels = {
            "identificativo": "Identificativo ",
            "data_scadenza": "Data Scadenza* ",
            "ente": "Ente* ",
        }
        widgets = {
            'data_scadenza': DateInput2(format='%Y-%m-%d')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['identificativo'].disabled = True


class form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(forms.Form):
    anno_inizio = forms.ChoiceField(
        choices=[(str(y), str(y)) for y in list(range(2050, 1970, -1))],
        label="Dall' Anno:",
        initial=str(datetime.now().year),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    mese_inizio = forms.ChoiceField(
        choices=[(str(m), nome) for m, nome in MESI_ITALIANI],
        label='Dal Mese:',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    anno_fine = forms.ChoiceField(
        choices=[(str(y), str(y)) for y in YEARS],
        label="All' Anno:",
        initial=str(datetime.now().year),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    mese_fine = forms.ChoiceField(
        choices=[(str(m), nome) for m, nome in MESI_ITALIANI],
        label=' Al Mese:',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    def clean(self):
        cleaned_data = super().clean()
        try:
            anno_inizio = int(cleaned_data.get('anno_inizio'))
            mese_inizio = int(cleaned_data.get('mese_inizio'))
            cleaned_data['data_inizio'] = f"{anno_inizio}-{mese_inizio:02d}-01"
            anno_fine = int(cleaned_data.get('anno_fine'))
            mese_fine = int(cleaned_data.get('mese_fine'))
            ultimo_giorno = calendar.monthrange(anno_fine, mese_fine)[1]
            cleaned_data['data_fine'] = f"{anno_fine}-{mese_fine:02d}-{ultimo_giorno:02d}"
            if cleaned_data['data_fine'] < cleaned_data['data_inizio']:
                raise ValidationError("La data di fine non può essere precedente alla data di inizio.")
        except (TypeError, ValueError):
            raise ValidationError("Errore nel formato dei campi anno o mese.")
        return cleaned_data
