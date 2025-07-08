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

class Protocollo(models.Model):
    identificativo = models.CharField(max_length=10, blank=True)
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False)  #obbligatorio
    #foreign_key
    cliente = models.ForeignKey(RubricaClienti, on_delete=models.CASCADE)  # obbligatorio
    referente = models.ForeignKey(RubricaReferenti, on_delete=models.SET_NULL, null=True, blank=True)
    indirizzo = models.CharField(max_length=100) #obbligatorio
    pratica = models.CharField(max_length=30)   #obbligatorio
    parcella = models.DecimalField(max_digits=14, decimal_places=2) #obbligatorio
    note = RichTextField(null=True, blank=True)
    data_scadenza = models.DateField(auto_now=False, auto_now_add=False, default=None) #obbligatorio
    data_consegna = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    status = models.IntegerField(default=None, null=True, blank=True)

    def __str__(self):
        return str(self.identificativo)+" | "+str(self.indirizzo)

    class Meta:
        ordering = ['-identificativo']

class Fattura(models.Model):
    identificativo = models.CharField(max_length=10)
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False)
    imponibile = models.DecimalField(max_digits=14, decimal_places=2)
    importo = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    # foreign_key
    protocollo = models.ForeignKey(Protocollo, on_delete=models.SET_NULL, related_name='fatture', null=True, blank=True)

    def __str__(self):
        return str(self.identificativo)

    class Meta:
        ordering = ['-identificativo']

class Ricavo(models.Model):
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    movimento = models.CharField(max_length=15, choices=(('ACCONTO', 'ACCONTO'),('SALDO', 'SALDO')), default="ACCONTO")
    importo = models.DecimalField(max_digits=14, decimal_places=2) #obbligatorio
    # foreign_key
    fattura = models.ForeignKey(Fattura, on_delete=models.SET_NULL, related_name="ricavi_fattura", null=True, blank=True)
    protocollo = models.ForeignKey(Protocollo, on_delete=models.SET_NULL, related_name="ricavi", null=True, blank=True)
    note = RichTextField(null=True, blank=True)
    destinazione = models.CharField(max_length=15, choices=(('DEPOSITO', 'DEPOSITO'),('CARTA', 'CARTA')), default="DEPOSITO")

    def __str__(self):
        return "id: "+str(self.id)

class SpesaCommessa(models.Model):
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    importo = models.DecimalField(max_digits=14, decimal_places=2) #obbligatorio
    # foreign_key
    protocollo = models.ForeignKey(Protocollo, on_delete=models.SET_NULL, related_name="spesecommessa", null=True, blank=True)
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

class Consulenza(models.Model):
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False)  #obbligatorio
    richiedente = models.CharField(max_length=40, null=True, blank=True)
    indirizzo = models.CharField(max_length=100)
    attivita = models.CharField(max_length=40)  #obbligatorio
    compenso = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    note = RichTextField(null=True, blank=True)
    data_scadenza = models.DateField(auto_now=False, auto_now_add=False, default=None)  #obbligatorio
    data_consegna = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    status = models.IntegerField(default=None, null=True, blank=True)



    # Da Fattura a Ricavo: Fattura.objects.get(id=1).ricavo (può essere None) possono esistere ricavi senza fattura
    # Da Fattura a Protocollo: Fattura.objects.get(id=1).protocollo (mai None) non possono esistere fatture senza protocollo

# class Ricavo(models.Model):
#     data_registrazione = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
#     movimento = models.CharField(max_length=15, choices=(('ACCONTO', 'ACCONTO'),('SALDO', 'SALDO')), default="ACCONTO")
#     importo = models.DecimalField(max_digits=14, decimal_places=2) #obbligatorio
#     note = RichTextField(null=True, blank=True)
#     destinazione = models.CharField(max_length=15, choices=(('DEPOSITO', 'DEPOSITO'),('CARTA', 'CARTA')), default="DEPOSITO")
#     fattura = models.OneToOneField(Fattura, on_delete=models.SET_NULL, null=True, blank=True, related_name='ricavo')
#     protocollo = models.ForeignKey(Protocollo, on_delete=models.SET_NULL, null=True, blank=True, related_name='ricavi')
#
#     def __str__(self):
#         return "id: "+str(self.id)

    # Da Ricavo alla Fattura: Ricavo.objects.get(id=1).fattura (può essere None) possono esistere fatture senza ricavi
    # Da Ricavo al Protocollo (diretto):  Ricavo.objects.get(id=1).protocollo (può essere None) possono esistere Ricavi non associati a Protocollo
    # Da Ricavo a Protocollo (tramite fattura) Ricavo.objects.get(id=1).fattura.protocollo (solo se il ricavo ha una fattura associata e quindi un protocollo associato)

    # @property
    # def protocollo_associato(self):
    #     # se è legato direttamente al protocollo
    #     if self.protocollo:
    #         return self.protocollo
    #     # altrimenti cerca tramite la fattura
    #     if self.fattura:
    #         return self.fattura.protocollo
    #     return None

    # ricavo.protocollo_associato  # restituisce il Protocollo, se c'è, da uno dei due canali


class CalendarioContatore(models.Model):
    count = models.IntegerField(default=0)
    fatture = models.IntegerField(default=0)
