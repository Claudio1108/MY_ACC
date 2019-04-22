from django import forms
from .models import *
from django.db import connection
import django_filters

class DateInput(forms.DateInput):
    input_type = 'date'


class formProtocol(forms.ModelForm):

    class Meta:

        model = Protocollo

        fields = "__all__"

        widgets = {
            'data': DateInput(),
        }

class formProtocolUpdate(forms.ModelForm):

    class Meta:

        model = Protocollo

        fields = "__all__"

        widgets = {
            'data': forms.DateInput(attrs={'class':'datepicker'}),
        }


class formGuadagno(forms.ModelForm):

    class Meta:

        model = Guadagno

        fields = "__all__"

        widgets = {
            'data': DateInput(),
        }

    def Check1(self):

        id_protocollo = self.data['protocollo']

        protocollo = Protocollo.objects.get(id=id_protocollo)


        query="""SELECT coalesce(sum(g.importo),0) as tot

                 FROM Contabilita_guadagno g

                 WHERE g.protocollo_id="""+str(id_protocollo)

        cursor = connection.cursor()
        cursor.execute(query);
        rows = cursor.fetchone()

        x=rows[0]

        y=int(self.data['importo'])

        z=protocollo.parcella

        if(x+y<=z):

            return True

        else:

            return False

class formGuadagnoUpdate(forms.ModelForm):

    class Meta:

        model = Guadagno

        fields = "__all__"

        widgets = {
            'data': forms.DateInput(attrs={'class':'datepicker'}),
        }

    def Check1(self):

        id_protocollo = self.data['protocollo']

        protocollo = Protocollo.objects.get(id=id_protocollo)


        query="""SELECT coalesce(sum(g.importo),0) as tot

                 FROM Contabilita_guadagno g

                 WHERE g.protocollo_id="""+str(id_protocollo)

        cursor = connection.cursor()
        cursor.execute(query);
        rows = cursor.fetchone()

        x=rows[0]

        y=int(self.data['importo'])

        z=protocollo.parcella

        if(x+y<=z):

            return True

        else:

            return False

class formSpesaCommessa(forms.ModelForm):

    class Meta:

        model = SpesaCommessa

        fields = "__all__"

        widgets = {
            'data': DateInput(),
        }

class formSpesaCommessaUpdate(forms.ModelForm):

    class Meta:

        model = SpesaCommessa

        fields = "__all__"

        widgets = {
            'data': forms.DateInput(attrs={'class':'datepicker'}),
        }

class formSocio(forms.ModelForm):

    class Meta:

        model = Socio

        fields = ["percentuale"]

class formSpesaGestione(forms.ModelForm):

    class Meta:

        model = SpesaGestione

        fields = "__all__"

        widgets = {
            'data': DateInput(),
        }

class formSpesaGestioneUpdate(forms.ModelForm):

    class Meta:

        model = SpesaGestione

        fields = "__all__"

        widgets = {
            'data': forms.DateInput(attrs={'class':'datepicker'}),
        }

class formRicavoEffettivo(forms.ModelForm):

    class Meta:

        model = RicavoEffettivo

        fields = "__all__"

        widgets = {
            'data': DateInput(),
        }

class formRicavoEffettivoUpdate(forms.ModelForm):

    class Meta:

        model = RicavoEffettivo

        fields = "__all__"

        widgets = {
            'data': forms.DateInput(attrs={'class':'datepicker'}),
        }

class formResocontoSpeseGestione(forms.Form):

    year = forms.IntegerField()


class formResocontoGuadagni(forms.Form):

    year = forms.IntegerField()

class formGestioneRicavi(forms.Form):

    year = forms.IntegerField()




