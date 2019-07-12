from django import forms
from .models import *
from django.db import connection

class DateInput(forms.DateInput):
    input_type = 'date'

class formProtocol(forms.ModelForm):
    class Meta:
        model = Protocollo
        fields = "__all__"
        labels = {
            "cliente": "Cliente ",
            "referente": "Referente ",
            "mail_cliente": "Mail Cliente ",
            "tel_cliente": "Tel Cliente ",
            "indirizzo": "Indirizzo ",
            "parcella": "Parcella* ",
            "pratica": "Pratica ",
            "note": "Note ",
            "data": "Data* "}
        widgets = {
            'data': DateInput(),
            'identificativo' : forms.HiddenInput()}

    def set_identificativo(self,value):
        data = self.data.copy()
        data['identificativo'] = value
        self.data = data

class formProtocolUpdate(forms.ModelForm):
    class Meta:
        model = Protocollo
        fields = "__all__"
        widgets = {
            'data': forms.DateInput(attrs={'class':'datepicker'})}

class formRicavo(forms.ModelForm):
    class Meta:
        model = Ricavo
        fields = ('data','movimento','importo','fattura','intestatario_fattura','causale','protocollo')
        labels = {
            "data": "Data* ",
            "movimento": "Movimento ",
            "importo": "Importo* ",
            "fattura": "Fattura ",
            "causale": "Causale ",
            "intestatario_fattura": "Intestatario Fattura ",
            "protocollo": "Protocollo "}
        widgets = {
            'data': DateInput()}

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
            'data': forms.DateInput(attrs={'class':'datepicker'})}

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
            "data": "Data* ",
            "importo": "Importo* ",
            "protocollo": "Protocollo "}
        widgets = {
            'data': DateInput()}

class formSpesaCommessaUpdate(forms.ModelForm):
    class Meta:
        model = SpesaCommessa
        fields = "__all__"
        widgets = {
            'data': forms.DateInput(attrs={'class':'datepicker'})}

class formSocio(forms.ModelForm):
    class Meta:
        model = Socio
        fields = ["percentuale"]

class formSpesaGestione(forms.ModelForm):
    class Meta:
        model = SpesaGestione
        fields = "__all__"
        labels = {
            "data": "Data* ",
            "importo": "Importo* ",
            "fattura": "Fattura ",
            "intestatario_fattura": "Intestatario Fattura ",
            "causale": "Causale "}
        widgets = {
            'data': DateInput()}

class formSpesaGestioneUpdate(forms.ModelForm):
    class Meta:
        model = SpesaGestione
        fields = "__all__"
        widgets = {
            'data': forms.DateInput(attrs={'class':'datepicker'})}

class formGuadagnoEffettivo(forms.ModelForm):
    class Meta:
        model = GuadagnoEffettivo
        fields = "__all__"
        labels = {
            "data": "Data* ",
            "importo": "Importo* "}
        widgets = {
            'data': DateInput()}

class formGuadagnoEffettivoUpdate(forms.ModelForm):
    class Meta:
        model = GuadagnoEffettivo
        fields = "__all__"
        widgets = {
            'data': forms.DateInput(attrs={'class':'datepicker'})}

class form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(forms.Form):
    year = forms.IntegerField()