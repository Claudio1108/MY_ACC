from django.db import models

class Protocollo(models.Model):
    identificativo = models.CharField(max_length=10, blank=True)
    cliente = models.CharField(max_length=25, blank=True)
    referente = models.CharField(max_length=25, blank=True)
    mail_cliente = models.EmailField(max_length=40, blank=True)
    tel_cliente = models.CharField(max_length=20, blank=True)
    indirizzo = models.CharField(max_length=40, blank=True)
    parcella = models.DecimalField(max_digits=19, decimal_places=2) #obbligatorio
    pratica = models.CharField(max_length=40, blank=True)
    note = models.TextField(blank=True)
    data_registrazione = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    data_concordata = models.DateField(auto_now=False, auto_now_add=False, default=None) #obbligatorio
    data_effettiva = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    status = models.IntegerField(default=None)

    def __str__(self):
        if(str(self.indirizzo) != ''):
            return str(self.identificativo)+" | "+str(self.indirizzo)
        else:
            return str(self.identificativo)+" | Not Specific Address"

    class Meta:
        ordering = ['-identificativo']

class Socio(models.Model):
    nome = models.CharField(max_length=25)
    cognome = models.CharField(max_length=25)
    percentuale = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.nome + " " + self.cognome

class Ricavo(models.Model):
    data = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    TIPO_MOVIMENTO = (('ACCONTO', 'ACCONTO'),('SALDO', 'SALDO'))
    movimento = models.CharField(max_length=10, choices=TIPO_MOVIMENTO,null=True, blank=True)
    importo = models.DecimalField(max_digits=19, decimal_places=2) #obbligatorio
    TIPO_FATTURA = (('SI', 'SI'),('NO', 'NO'))
    fattura = models.CharField(max_length=2, choices=TIPO_FATTURA, default='NO')
    causale = models.CharField(max_length=120,default="", null=True, blank=True)
    #foreign_key
    intestatario_fattura = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="sociofatturaricavo", default="", null=True, blank=True)
    #foreign_key
    protocollo = models.ForeignKey(Protocollo, on_delete=models.CASCADE, related_name="ricavi", default="", null=True, blank=True)
    #reated_name = relazione inversa, dato un protocollo vedere i relativi guadagni

    def __str__(self):
        return "id: "+str(self.id)

class SpesaCommessa(models.Model):

    data = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    importo = models.DecimalField(max_digits=19, decimal_places=2) #obbligatorio
    # foreign_key
    protocollo = models.ForeignKey(Protocollo, on_delete=models.CASCADE, related_name="spesecommessa")
    # reated_name = relazione inversa, dato un protocollo vedere i relativi guadagni

    def __str__(self):
        return "id: "+str(self.id)

class SpesaGestione(models.Model):
    data = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    importo = models.DecimalField(max_digits=19, decimal_places=2) #obbligatorio
    TIPO_FATTURA = (('SI', 'SI'),('NO', 'NO'))
    fattura = models.CharField(max_length=2, choices=TIPO_FATTURA, default='NO')
    # foreign_key
    intestatario_fattura = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="sociofatturaspesagestione", default="", null=True, blank=True)
    causale = models.CharField(max_length=120, default="", null=True, blank=True)

    def __str__(self):
        return "id: "+str(self.id)

class GuadagnoEffettivo(models.Model):
    data = models.DateField(auto_now=False, auto_now_add=False) #obbligatorio
    importo = models.DecimalField(max_digits=19, decimal_places=2) #obbligatorio

    def __str__(self):
        return "id: "+str(self.id)

class CalendarioContatore(models.Model):
    count = models.IntegerField()