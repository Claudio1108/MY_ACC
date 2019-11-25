from django.db import models
from ckeditor.fields import RichTextField

class RubricaClienti(models.Model):
    nominativo = models.CharField(max_length=40) #obbligatorio
    tel = models.CharField(max_length=20) #obbligatorio
    mail = models.EmailField(max_length=50, blank=True)
    note = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.nominativo + "/" + self.tel

class RubricaReferenti(models.Model):
    nominativo = models.CharField(max_length=40) #obbligatorio
    tel = models.CharField(max_length=20) #obbligatorio
    mail = models.EmailField(max_length=50, blank=True)
    note = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.nominativo + "/" + self.tel

class Socio(models.Model):
    nome = models.CharField(max_length=25)
    cognome = models.CharField(max_length=25)
    percentuale = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.nome + " " + self.cognome

class Protocollo(models.Model):
    identificativo = models.CharField(max_length=10, blank=True)
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False)  #obbligatorio
    #foreign_key
    cliente = models.ForeignKey(RubricaClienti, on_delete=models.CASCADE)  # obbligatorio
    referente = models.ForeignKey(RubricaReferenti, on_delete=models.CASCADE, null=True, blank=True)
    indirizzo = models.CharField(max_length=30) #obbligatorio
    pratica = models.CharField(max_length=30)   #obbligatorio
    parcella = models.DecimalField(max_digits=14, decimal_places=2) #obbligatorio
    note = RichTextField(null=True, blank=True)
    data_scadenza = models.DateField(auto_now=False, auto_now_add=False, default=None) #obbligatorio
    data_consegna = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    status = models.IntegerField(default=None)
    #foreign_key
    responsabile = models.ForeignKey(Socio, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.identificativo)+" | "+str(self.indirizzo)

    class Meta:
        ordering = ['-identificativo']

class Ricavo(models.Model):
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    movimento = models.CharField(max_length=15, choices=(('ACCONTO', 'ACCONTO'),('SALDO', 'SALDO')), default="ACCONTO")
    importo = models.DecimalField(max_digits=14, decimal_places=2) #obbligatorio
    fattura = models.CharField(max_length=2, choices=(('SI', 'SI'),('NO', 'NO')), default='NO')
    # foreign_key
    intestatario_fattura = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="sociofatturaricavo", null=True, blank=True)
    protocollo = models.ForeignKey(Protocollo, on_delete=models.CASCADE, related_name="ricavi", null=True, blank=True)
    note = RichTextField(null=True, blank=True)
    destinazione = models.CharField(max_length=15, choices=(('DEPOSITO', 'DEPOSITO'),('CARTA', 'CARTA')), default="DEPOSITO")

    def __str__(self):
        return "id: "+str(self.id)

class SpesaCommessa(models.Model):
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    importo = models.DecimalField(max_digits=14, decimal_places=2) #obbligatorio
    # foreign_key
    protocollo = models.ForeignKey(Protocollo, on_delete=models.CASCADE, related_name="spesecommessa", null=True,blank=True)
    note = RichTextField(null=True, blank=True)
    provenienza = models.CharField(max_length=15, choices=(('DEPOSITO', 'DEPOSITO'),('CARTA', 'CARTA')), default="DEPOSITO")

    def __str__(self):
        return "id: "+str(self.id)

class SpesaGestione(models.Model):
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    importo = models.DecimalField(max_digits=14, decimal_places=2) #obbligatorio
    causale = models.CharField(max_length=30, default="", null=True, blank=True)
    fattura = models.CharField(max_length=50, default="", null=True, blank=True)
    provenienza = models.CharField(max_length=15, choices=(('DEPOSITO', 'DEPOSITO'),('CARTA', 'CARTA')), default="DEPOSITO")

    def __str__(self):
        return "id: "+str(self.id)

class GuadagnoEffettivo(models.Model):
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    importo = models.DecimalField(max_digits=14, decimal_places=2) #obbligatorio
    provenienza = models.CharField(max_length=15, choices=(('DEPOSITO', 'DEPOSITO'),('CARTA', 'CARTA')), default="DEPOSITO")

    def __str__(self):
        return "id: "+str(self.id)

class Consulenza(models.Model):
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False)  #obbligatorio
    richiedente = models.CharField(max_length=40, null=True, blank=True)
    indirizzo = models.CharField(max_length=30)
    attivita = models.CharField(max_length=40)  #obbligatorio
    compenso = models.DecimalField(max_digits=14, decimal_places=2, blank=True, default=0)
    note = RichTextField(null=True, blank=True)
    data_scadenza = models.DateField(auto_now=False, auto_now_add=False, default=None)  #obbligatorio
    data_consegna = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    status = models.IntegerField(default=None)
    # foreign_key
    responsabile = models.ForeignKey(Socio, on_delete=models.CASCADE, null=True, blank=True)

class CalendarioContatore(models.Model):
    count = models.IntegerField()