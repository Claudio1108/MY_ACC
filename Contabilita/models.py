from django.db import models

class Protocollo(models.Model):
    identificativo = models.CharField(max_length=10, blank=True)
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False)  # obbligatorio
    cliente = models.CharField(max_length=25, blank=True)
    tel_cliente = models.CharField(max_length=20, blank=True)
    mail_cliente = models.EmailField(max_length=40, blank=True)
    referente = models.CharField(max_length=25, blank=True)
    tel_referente = models.CharField(max_length=20, blank=True)
    mail_referente = models.EmailField(max_length=40, blank=True)
    indirizzo = models.CharField(max_length=40) #obbligatorio
    pratica = models.CharField(max_length=40)   #obbligatorio
    parcella = models.DecimalField(max_digits=19, decimal_places=2) #obbligatorio
    note = models.TextField(blank=True)
    data_scadenza = models.DateField(auto_now=False, auto_now_add=False, default=None) #obbligatorio
    data_consegna = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    status = models.IntegerField(default=None)

    def __str__(self):
        return str(self.identificativo)+" | "+str(self.indirizzo)

    class Meta:
        ordering = ['-identificativo']

class Socio(models.Model):
    nome = models.CharField(max_length=25)
    cognome = models.CharField(max_length=25)
    percentuale = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.nome + " " + self.cognome

class Ricavo(models.Model):
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    movimento = models.CharField(max_length=10, choices=(('ACCONTO', 'ACCONTO'),('SALDO', 'SALDO')) ,null=True, blank=True)
    importo = models.DecimalField(max_digits=19, decimal_places=2) #obbligatorio
    fattura = models.CharField(max_length=2, choices=(('SI', 'SI'),('NO', 'NO')), default='NO')
    #foreign_key
    intestatario_fattura = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="sociofatturaricavo", default="", null=True, blank=True)
    #foreign_key
    protocollo = models.ForeignKey(Protocollo, on_delete=models.CASCADE, related_name="ricavi", default="", null=True, blank=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return "id: "+str(self.id)

class SpesaCommessa(models.Model):

    data_registrazione = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    importo = models.DecimalField(max_digits=19, decimal_places=2) #obbligatorio
    # foreign_key
    protocollo = models.ForeignKey(Protocollo, on_delete=models.CASCADE, related_name="spesecommessa")
    note = models.TextField(blank=True)

    def __str__(self):
        return "id: "+str(self.id)

class SpesaGestione(models.Model):
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    importo = models.DecimalField(max_digits=19, decimal_places=2) #obbligatorio
    causale = models.CharField(max_length=120, default="", null=True, blank=True)
    fattura = models.CharField(max_length=120, default="", null=True, blank=True)

    def __str__(self):
        return "id: "+str(self.id)

class GuadagnoEffettivo(models.Model):
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    importo = models.DecimalField(max_digits=19, decimal_places=2) #obbligatorio

    def __str__(self):
        return "id: "+str(self.id)

class CalendarioContatore(models.Model):
    count = models.IntegerField()