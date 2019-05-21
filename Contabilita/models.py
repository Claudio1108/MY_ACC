from django.db import models

# Create your models here.

class Protocollo(models.Model):
    identificativo = models.CharField(max_length=10, blank=True)
    cliente = models.CharField(max_length=25, blank=True)
    referente = models.CharField(max_length=25, blank=True)
    mail_cliente = models.EmailField(max_length=40, blank=True)
    tel_cliente = models.CharField(max_length=20, blank=True)
    indirizzo = models.CharField(max_length=40, blank=True)
    parcella = models.DecimalField(max_digits=19, decimal_places=2)
    pratica = models.CharField(max_length=40, blank=True)
    note = models.TextField(blank=True)
    data = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):

        return str(self.identificativo)+" | "+str(self.indirizzo)

class Socio(models.Model):

    nome = models.CharField(max_length=25)
    cognome = models.CharField(max_length=25)
    percentuale = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):

        return self.nome + " " + self.cognome

class Ricavo(models.Model):

    data = models.DateField(auto_now=False, auto_now_add=False)
    TIPO_MOVIMENTO = (
        ('ACCONTO', 'ACCONTO'),
        ('SALDO', 'SALDO')
    )
    movimento = models.CharField(max_length=10, choices=TIPO_MOVIMENTO, default='A')
    importo = models.DecimalField(max_digits=19, decimal_places=2)
    TIPO_FATTURA = (
        ('SI', 'SI'),
        ('NO', 'NO')

    )
    fattura = models.CharField(max_length=2, choices=TIPO_FATTURA, default='NO')
    #foreign_key
    intestatario_fattura = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="sociofatturaricavo", default="", null=True, blank=True)
    #foreign_key
    protocollo = models.ForeignKey(Protocollo, on_delete=models.CASCADE, related_name="ricavi", default="", null=True, blank=True)

    #reated_name = relazione inversa, dato un protocollo vedere i relativi guadagni

    def __str__(self):

        return self.importo

class SpesaCommessa(models.Model):

    data = models.DateField(auto_now=False, auto_now_add=False)
    importo = models.DecimalField(max_digits=19, decimal_places=2)

    # foreign_key
    protocollo = models.ForeignKey(Protocollo, on_delete=models.CASCADE, related_name="spesecommessa")
    # reated_name = relazione inversa, dato un protocollo vedere i relativi guadagni

    def __str__(self):

        return self.importo


class SpesaGestione(models.Model):

    data = models.DateField(auto_now=False, auto_now_add=False)
    importo = models.DecimalField(max_digits=19, decimal_places=2)
    TIPO_FATTURA = (
        ('SI', 'SI'),
        ('NO', 'NO')
    )
    fattura = models.CharField(max_length=2, choices=TIPO_FATTURA, default='NO')
    # foreign_key
    intestatario_fattura = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="sociofatturaspesagestione", default="", null=True, blank=True)
    causale = models.CharField(max_length=120)

    def __str__(self):

        return self.importo


class GuadagnoEffettivo(models.Model):

    data = models.DateField(auto_now=False, auto_now_add=False)
    importo = models.DecimalField(max_digits=19, decimal_places=2)

    def __str__(self):

        return self.importo

class CalendarioContatore(models.Model):

    count=models.IntegerField()