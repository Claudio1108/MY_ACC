from django.db import models
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator

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
    parcella = models.DecimalField(max_digits=14, decimal_places=2, validators = [MinValueValidator(0)]) #obbligatorio
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
    imponibile = models.DecimalField(max_digits=14, decimal_places=2, validators = [MinValueValidator(0)])
    importo = models.DecimalField(max_digits=14, decimal_places=2, validators = [MinValueValidator(0)], null=True)
    # foreign_key
    protocollo = models.ForeignKey(Protocollo, on_delete=models.SET_NULL, related_name='fatture', null=True, blank=True)

    def __str__(self):
        return str(self.identificativo)

    class Meta:
        ordering = ['-identificativo']

class Ricavo(models.Model):
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    movimento = models.CharField(max_length=15, choices=(('ACCONTO', 'ACCONTO'),('SALDO', 'SALDO')), default="ACCONTO")
    importo = models.DecimalField(max_digits=14, decimal_places=2, validators = [MinValueValidator(0)]) #obbligatorio
    # foreign_key
    fattura = models.ForeignKey(Fattura, on_delete=models.SET_NULL, related_name="ricavi_fattura", null=True, blank=True)
    protocollo = models.ForeignKey(Protocollo, on_delete=models.SET_NULL, related_name="ricavi", null=True, blank=True)
    note = RichTextField(null=True, blank=True)
    destinazione = models.CharField(max_length=15, choices=(('DEPOSITO', 'DEPOSITO'),('CARTA', 'CARTA')), default="DEPOSITO")

    def __str__(self):
        return "id: "+str(self.id)

class SpesaCommessa(models.Model):
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    importo = models.DecimalField(max_digits=14, decimal_places=2, validators = [MinValueValidator(0)]) #obbligatorio
    # foreign_key
    protocollo = models.ForeignKey(Protocollo, on_delete=models.SET_NULL, related_name="spesecommessa", null=True, blank=True)
    note = RichTextField(null=True, blank=True)
    provenienza = models.CharField(max_length=15, choices=(('DEPOSITO', 'DEPOSITO'),('CARTA', 'CARTA')), default="DEPOSITO")

    def __str__(self):
        return "id: "+str(self.id)

class Consulenza(models.Model):
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False)  #obbligatorio
    richiedente = models.CharField(max_length=40, null=True, blank=True)
    indirizzo = models.CharField(max_length=100)
    attivita = models.CharField(max_length=40)  #obbligatorio
    compenso = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators = [MinValueValidator(0)])
    note = RichTextField(null=True, blank=True)
    data_scadenza = models.DateField(auto_now=False, auto_now_add=False, default=None)  #obbligatorio
    data_consegna = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    status = models.IntegerField(default=None, null=True, blank=True)

class F24(models.Model):
    data_scadenza = models.DateField(auto_now=False, auto_now_add=False, default=None) #obbligatorio
    identificativo = models.CharField(max_length=50, unique=True) #obbligatorio
    ente = models.CharField(max_length=15, choices=(('AdE', 'AdE'), ('INARCASSA', 'INARCASSA')), null=False,
                            blank=False)  # obbligatorio

    def __str__(self):
        return f"F24 - {self.identificativo}"

class CodiceTributo(models.Model):
    MESE_CHOICES = [
        ('Gennaio', 'Gennaio'),
        ('Febbraio', 'Febbraio'),
        ('Marzo', 'Marzo'),
        ('Aprile', 'Aprile'),
        ('Maggio', 'Maggio'),
        ('Giugno', 'Giugno'),
        ('Luglio', 'Luglio'),
        ('Agosto', 'Agosto'),
        ('Settembre', 'Settembre'),
        ('Ottobre', 'Ottobre'),
        ('Novembre', 'Novembre'),
        ('Dicembre', 'Dicembre'),
    ]
    ANNO_CHOICES = [(anno, str(anno)) for anno in range(2050, 1969, -1)]
    anno = models.PositiveIntegerField(choices=ANNO_CHOICES, null=False, blank=False) # obbligatorio
    mese = models.CharField(max_length=10, choices=MESE_CHOICES, null=True, blank=True)
    identificativo = models.CharField(max_length=50, null=False, blank=False) # obbligatorio
    debito = models.DecimalField(max_digits=14, decimal_places=2, validators = [MinValueValidator(0)], null=True, blank=True)
    credito =  models.DecimalField(max_digits=14, decimal_places=2, validators = [MinValueValidator(0)], null=True, blank=True)
    # foreign_key
    f24 = models.ForeignKey(F24, on_delete=models.CASCADE, related_name='codicetributo', null=False, blank=False) # obbligatorio

    def __str__(self):
        return f"{self.identificativo}"

class SpesaGestione(models.Model):
    identificativo = models.CharField(max_length=50, null=False, blank=False)  # obbligatorio
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    importo = models.DecimalField(max_digits=14, decimal_places=2, validators = [MinValueValidator(0)]) #obbligatorio
    causale = models.CharField(max_length=30, default="", null=True, blank=True)
    fattura = models.CharField(max_length=50, default="", null=True, blank=True)
    provenienza = models.CharField(max_length=15, choices=(('DEPOSITO', 'DEPOSITO'),('CARTA', 'CARTA')), default="DEPOSITO")
    f24 = models.OneToOneField(
        F24,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='spesagestione'
    )

    def __str__(self):
        return f"{self.identificativo} | {self.data_registrazione} | {self.importo} €"

class CalendarioContatore(models.Model):
    count = models.IntegerField(default=0)
    fatture = models.IntegerField(default=0)
