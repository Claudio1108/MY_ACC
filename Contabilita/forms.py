from django import forms
from .models import *
from django.db import connection

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


class formClienteUpdate(forms.ModelForm):
    class Meta:
        model = RubricaClienti
        fields = "__all__"

class formReferente(forms.ModelForm):
    class Meta:
        model = RubricaReferenti
        fields = "__all__"
        labels = {
            "nominativo": "Azienda - Nome - Cognome* ",
            "tel": "Telefono* ",
            "mail": "Mail ",
            "note": "Note "}


class formReferenteUpdate(forms.ModelForm):
    class Meta:
        model = RubricaReferenti
        fields = "__all__"

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
            "data_consegna": "Data Consegna "}
        widgets = {
            'data_registrazione': DateInput(),
            'data_scadenza': DateInput(),
            'data_consegna': DateInput(),
            'identificativo' : forms.HiddenInput(),
            'status' : forms.HiddenInput()}

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
        widgets = {
            'data_registrazione': forms.DateInput(attrs={'class':'datepicker'}),
            'identificativo': forms.HiddenInput(),
            'status': forms.HiddenInput()}

class formConsulenza(forms.ModelForm):
    class Meta:
        model = Consulenza
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "cliente": "Cliente ",
            "indirizzo": "Indirizzo* ",
            "attivita": "Attività* ",
            "compenso": "Compenso ",
            "note": "Note ",
            "data_scadenza": "Data Scadenza* ",
            "data_consegna": "Data Consegna "}
        widgets = {
            'data_registrazione': DateInput(),
            'data_scadenza': DateInput(),
            'data_consegna': DateInput(),
            'status' : forms.HiddenInput()}

    def set_status(self,value):
        data = self.data.copy()
        data['status'] = value
        self.data = data


class formConsulenzaUpdate(forms.ModelForm):
    class Meta:
        model = Consulenza
        fields = "__all__"
        widgets = {
            'data_registrazione': forms.DateInput(attrs={'class':'datepicker'}),
            'status': forms.HiddenInput()}

class formRicavo(forms.ModelForm):
    class Meta:
        model = Ricavo
        fields = ('data_registrazione','movimento','importo','fattura','intestatario_fattura', 'protocollo', 'note')
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "movimento": "Movimento ",
            "importo": "Importo* ",
            "fattura": "Fattura ",
            "intestatario_fattura": "Intestatario Fattura ",
            "protocollo": "Protocollo ",
            "note": "Note "}
        widgets = {
            'data_registrazione': DateInput()}

    def Check1(self):
        id_protocollo = self.data['protocollo']
        protocollo = Protocollo.objects.get(id=id_protocollo)
        query="""SELECT coalesce(sum(r.importo),0) as tot
                 FROM Contabilita_ricavo r
                 WHERE r.protocollo_id={}""".format(str(id_protocollo))

        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchone()

        x=rows[0]
        y=int(self.data['importo'])
        z=protocollo.parcella
        if(x+y<=z):
            return True
        else:
            return False

class formRicavoUpdate(forms.ModelForm):
    class Meta:
        model = Ricavo
        fields = "__all__"
        widgets = {
            'data_registrazione': forms.DateInput(attrs={'class':'datepicker'})}

    def Check1(self):
        id_protocollo = self.data['protocollo']
        protocollo = Protocollo.objects.get(id=id_protocollo)
        query="""SELECT coalesce(sum(r.importo),0) as tot
                 FROM Contabilita_ricavo r
                 WHERE r.protocollo_id={}""".format(str(id_protocollo))

        cursor = connection.cursor()
        cursor.execute(query);
        rows = cursor.fetchone()

        x=rows[0]
        y=float(self.data['importo'])
        z=protocollo.parcella
        if(x+y<=z):
            return True
        else:
            return False

class formSpesaCommessa(forms.ModelForm):
    class Meta:
        model = SpesaCommessa
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "importo": "Importo* ",
            "protocollo": "Protocollo ",
            "note": "Note "}
        widgets = {
            'data_registrazione': DateInput()}

class formSpesaCommessaUpdate(forms.ModelForm):
    class Meta:
        model = SpesaCommessa
        fields = "__all__"
        widgets = {
            'data_registrazione': forms.DateInput(attrs={'class':'datepicker'})}

class formSocio(forms.ModelForm):
    class Meta:
        model = Socio
        fields = ["percentuale"]

class formSpesaGestione(forms.ModelForm):
    class Meta:
        model = SpesaGestione
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "importo": "Importo* ",
            "causale": "Causale ",
            "fattura": "Fattura ",}
        widgets = {
            'data_registrazione': DateInput()}

class formSpesaGestioneUpdate(forms.ModelForm):
    class Meta:
        model = SpesaGestione
        fields = "__all__"
        widgets = {
            'data_registrazione': forms.DateInput(attrs={'class':'datepicker'})}

class formGuadagnoEffettivo(forms.ModelForm):
    class Meta:
        model = GuadagnoEffettivo
        fields = "__all__"
        labels = {
            "data_registrazione": "Data* ",
            "importo": "Importo* "}
        widgets = {
            'data_registrazione': DateInput()}

class formGuadagnoEffettivoUpdate(forms.ModelForm):
    class Meta:
        model = GuadagnoEffettivo
        fields = "__all__"
        widgets = {
            'data_registrazione': forms.DateInput(attrs={'class':'datepicker'})}

class form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(forms.Form):
    year = forms.IntegerField(required = True)