import re
from datetime import datetime
from django import forms
from .models import *
from dal import autocomplete
from Contabilita import sqlite_queries as sqlite

YEARS = [x for x in range(1970, 2050)]

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
            'data_registrazione': forms.SelectDateWidget(years=YEARS),
            'data_scadenza': forms.SelectDateWidget(years=YEARS),
            'data_consegna': forms.SelectDateWidget(years=YEARS),
            'identificativo': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'cliente': autocomplete.ModelSelect2(url='cliente_autocomp'),
            'referente': autocomplete.ModelSelect2(url='referente_autocomp')
        }

    def check_date(self):
        data = self.data.copy()
        registrazione = datetime.strptime(
            f"{data['data_registrazione_day']}/{data['data_registrazione_month']}/{data['data_registrazione_year']}",
            "%d/%m/%Y").strftime("%Y-%m-%d")
        scadenza = datetime.strptime(
            f"{data['data_scadenza_day']}/{data['data_scadenza_month']}/{data['data_scadenza_year']}",
            "%d/%m/%Y").strftime("%Y-%m-%d")
        consegna = (
            datetime.strptime(f"{data['data_consegna_day']}/{data['data_consegna_month']}/{data['data_consegna_year']}",
                              "%d/%m/%Y").strftime("%Y-%m-%d")
            if data["data_consegna_day"] and data['data_consegna_month'] and data['data_consegna_year']
            else ""
        )
        return scadenza >= registrazione and (consegna >= registrazione if consegna else True)

    def set_identificativo(self,value):
        data = self.data.copy()
        data['identificativo'] = value
        self.data = data

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
            "compenso": "Compenso* ",
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
            "data_consegna": "Data Consegna ",
            "responsabile": "Responsabile "}
        widgets = {
            'data_registrazione': forms.SelectDateWidget(years=YEARS),
            'data_scadenza': forms.SelectDateWidget(years=YEARS),
            'data_consegna': forms.SelectDateWidget(years=YEARS),
            'status': forms.HiddenInput()}

    def check_date(self):
        data = self.data.copy()
        registrazione = datetime.strptime(
            f"{data['data_registrazione_day']}/{data['data_registrazione_month']}/{data['data_registrazione_year']}",
            "%d/%m/%Y").strftime("%Y-%m-%d")
        scadenza = datetime.strptime(
            f"{data['data_scadenza_day']}/{data['data_scadenza_month']}/{data['data_scadenza_year']}",
            "%d/%m/%Y").strftime("%Y-%m-%d")
        consegna = (
            datetime.strptime(f"{data['data_consegna_day']}/{data['data_consegna_month']}/{data['data_consegna_year']}",
                              "%d/%m/%Y").strftime("%Y-%m-%d")
            if data["data_consegna_day"] and data['data_consegna_month'] and data['data_consegna_year']
            else ""
        )
        return scadenza >= registrazione and (consegna >= registrazione if consegna else True)

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
            "destinazione": "Destinazione "}
        widgets = {
            'data_registrazione': forms.SelectDateWidget(years=YEARS),
            'protocollo': autocomplete.ModelSelect2(url='proto_autocomp')}

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
            'data_registrazione': forms.SelectDateWidget(years=YEARS),
            'protocollo': autocomplete.ModelSelect2(url='proto_autocomp')}

class formSocio(forms.ModelForm):
    class Meta:
        model = Socio
        fields = ["percentuale"]
        labels = {"percentuale": ""}

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
        widgets = {'data_registrazione': DateInput()}

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
        widgets = {'data_registrazione': forms.SelectDateWidget(years=YEARS),}

class formGuadagnoEffettivo(forms.ModelForm):
    class Meta:
        model = GuadagnoEffettivo
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "importo": "Importo* ",
            "provenienza": "Provenienza "}
        widgets = {'data_registrazione': DateInput()}

class formGuadagnoEffettivoUpdate(forms.ModelForm):
    class Meta:
        model = GuadagnoEffettivo
        fields = "__all__"
        labels = {
            "data_registrazione": "Data Registrazione* ",
            "importo": "Importo* ",
            "provenienza": "Provenienza "}
        widgets = {'data_registrazione': forms.SelectDateWidget(years=YEARS),}

class form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(forms.Form):
    year = forms.IntegerField(required = True, initial=datetime.now().year, label='Anno')