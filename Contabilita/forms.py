import re
from datetime import datetime
from django import forms
from .models import *
from django.db import connection
from dal import autocomplete

class DateInput(forms.DateInput):
    input_type = 'date'

class formCliente(forms.ModelForm):
    class Meta:
        model = RubricaClienti
        fields = "__all__"
        labels = {
            "nominativo": "Nome - Cognome* ",
            "tel": "Telefono* ",
            "mail": "Mail ",
            "note": "Note "}

class formReferente(forms.ModelForm):
    class Meta:
        model = RubricaReferenti
        fields = "__all__"
        labels = {
            "nominativo": "Azienda - Nome - Cognome* ",
            "tel": "Telefono* ",
            "mail": "Mail ",
            "note": "Note "}

class formProtocol(forms.ModelForm):
    class Meta:
        model = Protocollo
        fields = "__all__"
        labels = {
            "cliente": "Cliente* ",
            "referente": "Referente ",
            "indirizzo": "Indirizzo* ",
            "parcella": "Parcella* ",
            "pratica": "Pratica* ",
            "note": "Note ",
            "data_registrazione": "Data Registrazione* ",
            "data_scadenza": "Data Scadenza* ",
            "data_consegna": "Data Consegna ",
            "responsabile": "Responsabile "
        }
        widgets = {
            'data_registrazione': DateInput(),
            'data_scadenza': DateInput(),
            'data_consegna': DateInput(),
            'identificativo' : forms.HiddenInput(),
            'status' : forms.HiddenInput(),
            'cliente': autocomplete.ModelSelect2(url='cliente_autocomp'),
            'referente': autocomplete.ModelSelect2(url='referente_autocomp')}

    def check_date(self):
        data = self.data.copy()
        return data['data_scadenza'] >= data['data_registrazione'] or data['data_consegna'] >= data['data_registrazione']

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
        labels = {
            "cliente": "Cliente* ",
            "referente": "Referente ",
            "indirizzo": "Indirizzo* ",
            "parcella": "Parcella* ",
            "pratica": "Pratica* ",
            "note": "Note ",
            "data_registrazione": "Data Registrazione* ",
            "data_scadenza": "Data Scadenza* ",
            "data_consegna": "Data Consegna ",
            "responsabile": "Responsabile "
        }
        widgets = {
            'data_registrazione': forms.DateInput(attrs={'class':'datepicker'}),
            'identificativo': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'cliente': autocomplete.ModelSelect2(url='cliente_autocomp'),
            'referente': autocomplete.ModelSelect2(url='referente_autocomp')
        }

    def check_date(self):
        data = self.data.copy()
        registrazione = datetime.strptime(data['data_registrazione'], '%d/%m/%Y').strftime('%Y-%m-%d')
        scadenza = datetime.strptime(data['data_scadenza'], '%d/%m/%Y').strftime('%Y-%m-%d')
        consegna = datetime.strptime(data['data_consegna'], '%d/%m/%Y').strftime('%Y-%m-%d') if data['data_consegna'] else ''
        return scadenza >= registrazione or consegna >= registrazione

    def set_status(self,value):
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
            "compenso": "Compenso ",
            "note": "Note ",
            "data_scadenza": "Data Scadenza* ",
            "data_consegna": "Data Consegna ",
            "responsabile": "Responsabile "}
        widgets = {
            'data_registrazione': DateInput(),
            'data_scadenza': DateInput(),
            'data_consegna': DateInput(),
            'status' : forms.HiddenInput()}

    def check_date(self):
        data = self.data.copy()
        return data['data_scadenza'] >= data['data_registrazione'] or data['data_consegna'] >= data['data_registrazione']

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
            "compenso": "Compenso ",
            "note": "Note ",
            "data_scadenza": "Data Scadenza* ",
            "data_consegna": "Data Consegna ",
            "responsabile": "Responsabile "}
        widgets = {
            'data_registrazione': forms.DateInput(attrs={'class':'datepicker'}),
            'status': forms.HiddenInput()}

    def check_date(self):
        data = self.data.copy()
        registrazione = datetime.strptime(data['data_registrazione'], '%d/%m/%Y').strftime('%Y-%m-%d')
        scadenza = datetime.strptime(data['data_scadenza'], '%d/%m/%Y').strftime('%Y-%m-%d')
        consegna = datetime.strptime(data['data_consegna'], '%d/%m/%Y').strftime('%Y-%m-%d') if data['data_consegna'] else ''
        return scadenza >= registrazione or consegna >= registrazione

    def set_status(self, value):
        data = self.data.copy()
        data['status'] = value
        self.data = data

class formRicavo(forms.ModelForm):
    class Meta:
        model = Ricavo
        fields = ('data_registrazione','movimento','importo','fattura','intestatario_fattura', 'protocollo', 'note', 'destinazione')
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "movimento": "Movimento ",
            "importo": "Importo* ",
            "fattura": "Fattura ",
            "intestatario_fattura": "Intestatario Fattura ",
            "protocollo": "Protocollo ",
            "note": "Note ",
            "destinazione": "Destinazione "}
        widgets = {
            'data_registrazione': DateInput(),
            'protocollo': autocomplete.ModelSelect2(url='proto_autocomp')}

    def Check1(self):
        id_protocollo = self.data['protocollo']
        protocollo = Protocollo.objects.get(id=id_protocollo)
        query="""SELECT coalesce(sum(r.importo),0) as tot
                 FROM Contabilita_ricavo r
                 WHERE r.protocollo_id={}""".format(str(id_protocollo))
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchone()
        return rows[0] + int(self.data['importo']) <= protocollo.parcella

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
            "destinazione": "Destinazione "}
        widgets = {
            'data_registrazione': forms.DateInput(attrs={'class':'datepicker'}),
            'protocollo': autocomplete.ModelSelect2(url='proto_autocomp')}

    def Check2(self, id_ricavo):
        id_protocollo = self.data['protocollo']
        protocollo = Protocollo.objects.get(id=id_protocollo)
        query="""SELECT coalesce(sum(r.importo),0) as tot
                 FROM Contabilita_ricavo r
                 WHERE r.protocollo_id={} AND r.id!={}""".format(str(id_protocollo), re.findall("(\d+)", str(id_ricavo))[0])
        cursor = connection.cursor()
        cursor.execute(query);
        rows = cursor.fetchone()
        return rows[0] + float(self.data['importo']) <= protocollo.parcella

class formSpesaCommessa(forms.ModelForm):
    class Meta:
        model = SpesaCommessa
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "importo": "Importo* ",
            "protocollo": "Protocollo ",
            "note": "Note ",
            "provenienza": "Provenienza "}
        widgets = {
            'data_registrazione': DateInput(),
            'protocollo': autocomplete.ModelSelect2(url='proto_autocomp')}

class formSpesaCommessaUpdate(forms.ModelForm):
    class Meta:
        model = SpesaCommessa
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "importo": "Importo* ",
            "protocollo": "Protocollo ",
            "note": "Note ",
            "provenienza": "Provenienza "}
        widgets = {
            'data_registrazione': forms.DateInput(attrs={'class':'datepicker'}),
            'protocollo': autocomplete.ModelSelect2(url='proto_autocomp')}

class formSocio(forms.ModelForm):
    class Meta:
        model = Socio
        fields = ["percentuale"]
        labels = {
            "percentuale": ""}

class formSpesaGestione(forms.ModelForm):
    class Meta:
        model = SpesaGestione
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "importo": "Importo* ",
            "causale": "Causale ",
            "fattura": "Fattura ",
            "provenienza": "Provenienza "}
        widgets = {
            'data_registrazione': DateInput()}

class formSpesaGestioneUpdate(forms.ModelForm):
    class Meta:
        model = SpesaGestione
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "importo": "Importo* ",
            "causale": "Causale ",
            "fattura": "Fattura ",
            "provenienza": "Provenienza "}
        widgets = {
            'data_registrazione': forms.DateInput(attrs={'class':'datepicker'})}

class formGuadagnoEffettivo(forms.ModelForm):
    class Meta:
        model = GuadagnoEffettivo
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "importo": "Importo* ",
            "provenienza": "Provenienza "}
        widgets = {
            'data_registrazione': DateInput()}

class formGuadagnoEffettivoUpdate(forms.ModelForm):
    class Meta:
        model = GuadagnoEffettivo
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "importo": "Importo* ",
            "provenienza": "Provenienza "}
        widgets = {
            'data_registrazione': forms.DateInput(attrs={'class':'datepicker'})}

class form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(forms.Form):
    year = forms.IntegerField(required = True, initial=datetime.now().year, label='Anno')