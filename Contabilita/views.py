import xlwt
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .filters import *
from datetime import date, datetime
from django.http import HttpResponse
from dal import autocomplete
from Contabilita import sqlite_queries as sqlite

class ProtocolloAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Protocollo.objects.all().order_by('identificativo')
        return qs.filter(identificativo__icontains=self.q) | qs.filter(indirizzo__icontains=self.q) if self.q else qs

class FatturaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Fattura.objects.all().order_by('identificativo')
        return qs.filter(identificativo__icontains=self.q) if self.q else qs

class ClienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = RubricaClienti.objects.all().order_by('nominativo')
        return qs.filter(nominativo__icontains=self.q) | qs.filter(tel__icontains=self.q) if self.q else qs

class ReferenteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = RubricaReferenti.objects.all().order_by('nominativo')
        return qs.filter(nominativo__icontains=self.q) | qs.filter(tel__icontains=self.q) if self.q else qs

@login_required
def viewHomePage(request):
    return render(request, "Homepage/HomePage.html", {"user": request.user})

@login_required
def viewHomePageContabilita(request):
    return render(request, "Homepage/HomePageContabilita.html")

@login_required
def viewHomePageAmministrazione(request):
    context = {
        'count_active_protocols': Protocollo.objects.filter(data_consegna__isnull=True).count(),
        'count_deactive_protocols': Protocollo.objects.filter(data_consegna__isnull=False).count(),
        'count_clients': RubricaClienti.objects.count(),
        'count_referents': RubricaReferenti.objects.count(),
        'count_active_consultancies': Consulenza.objects.filter(data_consegna__isnull=True).count(),
        'count_deactive_consultancies': Consulenza.objects.filter(data_consegna__isnull=False).count(),
    }
    return render(request, "Homepage/HomePageAmministrazione.html", context)

@login_required
def viewAllClienti(request):
    cliente_filter = ClienteFilter(request.GET, queryset=RubricaClienti.objects.all().order_by("nominativo"))
    return render(request, "Amministrazione/Cliente/AllClienti.html", {"filter": cliente_filter, "filter_queryset": list(cliente_filter.qs)})

@login_required
def viewCreateCliente(request):
    if (request.method == "POST"):
        form = formCliente(request.POST)
        if (form.is_valid()):
            form.save()
            return redirect('AllClienti')
        else:
            return render(request, "Amministrazione/Cliente/CreateCliente.html", {'form': form})
    else:
        return render(request, "Amministrazione/Cliente/CreateCliente.html", {'form': formCliente()})

@login_required
def viewDeleteCliente(id):
    RubricaClienti.objects.get(id=id).delete()
    return redirect('AllClienti')

@login_required
def viewDeleteClientiGroup(request):
    if request.method == "POST":
        for task in request.POST.getlist('list[]'):
            RubricaClienti.objects.get(id=int(task)).delete()
    return render(request, "Homepage/HomePageAmministrazione.html")

@login_required
def viewUpdateCliente(request, id):
    if (request.method == "POST"):
        form = formCliente(request.POST, instance=RubricaClienti.objects.get(id=id))
        if (form.is_valid()):
            form.save()
            return redirect('AllClienti')
        else:
            return render(request, "Amministrazione/Cliente/UpdateCliente.html", {'form': form})
    else:
        return render(request, "Amministrazione/Cliente/UpdateCliente.html", {'form': formCliente(instance=RubricaClienti.objects.get(id=id))})

@login_required
def viewAllReferenti(request):
    referente_filter = ReferenteFilter(request.GET, queryset=RubricaReferenti.objects.all().order_by("nominativo"))
    return render(request, "Amministrazione/Referente/AllReferenti.html",{"filter": referente_filter, "filter_queryset": list(referente_filter.qs)})

@login_required
def viewCreateReferente(request):
    if (request.method == "POST"):
        form = formReferente(request.POST)
        if (form.is_valid()):
            form.save()
            return redirect('AllReferenti')
        else:
            return render(request, "Amministrazione/Referente/CreateReferente.html", {'form': form})
    else:
        return render(request, "Amministrazione/Referente/CreateReferente.html", {'form': formReferente()})

@login_required
def viewDeleteReferente(request, id):
    RubricaReferenti.objects.get(id=id).delete()
    return redirect('AllReferenti')

@login_required
def viewDeleteReferentiGroup(request):
    if request.method == "POST":
        for task in request.POST.getlist('list[]'):
            RubricaReferenti.objects.get(id=int(task)).delete()
    return render(request, "Homepage/HomePageAmministrazione.html")

@login_required
def viewUpdateReferente(request, id):
    if (request.method == "POST"):
        form = formReferente(request.POST, instance=RubricaReferenti.objects.get(id=id))
        if (form.is_valid()):
            form.save()
            return redirect('AllReferenti')
        else:
            return render(request, "Amministrazione/Referente/UpdateReferente.html", {'form': form})
    else:
        return render(request, "Amministrazione/Referente/UpdateReferente.html", {'form': formReferente(instance=RubricaReferenti.objects.get(id=id))})

@login_required
def viewAllProtocols(request):
    protocollo_filter = ProtocolloFilter(request.GET, queryset=Protocollo.objects.all().order_by("-data_registrazione__year", "-identificativo"))
    for proto in protocollo_filter.qs:
        data_scadenza = datetime.strptime(str(proto.data_scadenza), "%Y-%m-%d").date()
        if proto.data_consegna != None:
            proto.status = None
        else:
            proto.status = (data_scadenza - date.today()).days
            Protocollo.objects.filter(identificativo=proto.identificativo).update(status=proto.status)
    sum_parcelle = round(protocollo_filter.qs.aggregate(Sum('parcella'))['parcella__sum'] or 0, 2)
    return render(request, "Amministrazione/Protocollo/AllProtocols.html", {"filter": protocollo_filter, 'filter_queryset': list(protocollo_filter.qs), 'sum_p': sum_parcelle})

@login_required
def viewCreateProtocol(request):
    if (request.method == "POST"):
        form = formProtocol(request.POST)
        anno = form['data_registrazione'].value()[0:4]
        progressive_number_calendar = CalendarioContatore.objects.filter(id=anno).values('count')[0]['count']
        CalendarioContatore.objects.filter(id=anno).update(count=progressive_number_calendar + 1)
        form.set_identificativo(str('{0:03}'.format(progressive_number_calendar + 1)) + "-" + anno[2:4])
        data_scadenza = datetime.strptime(form['data_scadenza'].value(), "%Y-%m-%d").date()
        form.set_status(None if form['data_consegna'].value() != '' else (data_scadenza - date.today()).days)
        if (form.check_date()):
            if (form.is_valid()):
                form.save()
                return redirect('AllProtocols')
            else:
                CalendarioContatore.objects.filter(id=anno).update(count=progressive_number_calendar)
                return render(request, "Amministrazione/Protocollo/CreateProtocol.html", {'form': form})
        else:
            CalendarioContatore.objects.filter(id=anno).update(count=progressive_number_calendar)
            messages.error(request, 'ATTENZIONE! La Data di Scadenza e la Data di Consegna devono essere necessariamente successive o uguali alla Data di Registrazione.')
            return render(request, "Amministrazione/Protocollo/CreateProtocol.html", {'form': form})
    else:
        return render(request, "Amministrazione/Protocollo/CreateProtocol.html", {'form': formProtocol()})

@login_required
def viewDeleteProtocol(id):
    Protocollo.objects.get(id=id).delete()
    return redirect('AllProtocols')

@login_required
def viewDeleteProtocolsGroup(request):
    if request.method == "POST":
        for task in request.POST.getlist('list[]'):
            Protocollo.objects.get(id=int(task)).delete()
    return render(request, "Homepage/HomePageAmministrazione.html")

@login_required
def viewUpdateProtocol(request, id):
    protocollo = Protocollo.objects.get(id=id)
    if (request.method == "POST"):
        form = formProtocolUpdate(request.POST, instance=protocollo)
        anno = form['data_registrazione'].value()[:4]
        progressive_number_calendar = CalendarioContatore.objects.filter(id=anno).values('count')[0]['count']
        anno_pre = str(protocollo.data_registrazione.year)
        if anno != anno_pre:
            CalendarioContatore.objects.filter(id=anno).update(count=progressive_number_calendar + 1)
            form.set_identificativo(str('{0:03}'.format(progressive_number_calendar + 1)) + "-" + anno[2:4])
        data_scadenza = datetime.strptime(form['data_scadenza'].value(), "%Y-%m-%d").date()
        form.set_status(None if form['data_consegna'].value() != '' else (data_scadenza - date.today()).days)
        if (form.check_date()):
            nuova_parcella = float(form['parcella'].value() or 0)

            # CONTROLLO: Somma importi FATTURE associate al protocollo
            fatture = Fattura.objects.filter(protocollo=protocollo)
            totale_fatture = sum(float(f.importo or 0) for f in fatture)
            if totale_fatture > nuova_parcella:
                messages.error(
                    request,
                    f"ATTENZIONE! La parcella inserita ({nuova_parcella:.2f} €) è inferiore alla somma delle fatture associate ({totale_fatture:.2f} €)."
                )
                anno != anno_pre and CalendarioContatore.objects.filter(id=anno).update(
                    count=progressive_number_calendar + 1)
                return render(request, "Amministrazione/Protocollo/UpdateProtocol.html", {'form': form})

            if form.check_ricavi_on_protocollo(id, nuova_parcella):
                if (form.is_valid()):
                    form.save()
                    anno != anno_pre and protocollo.update(identificativo=str('{0:03}'.format(progressive_number_calendar + 1))+ "-" + anno[2:4])
                    return redirect('AllProtocols')
                else:
                    anno != anno_pre and CalendarioContatore.objects.filter(id=anno).update(count=progressive_number_calendar + 1)
                    return render(request, "Amministrazione/Protocollo/UpdateProtocol.html", {'form': form})
            else:
                anno != anno_pre and CalendarioContatore.objects.filter(id=anno).update(
                    count=progressive_number_calendar + 1)
                messages.error(request,
                               f"ATTENZIONE! La somma degli importi dei ricavi associati al protocollo {form['identificativo'].value()} supera il valore della parcella inserito di {form['parcella'].value()}")
                return render(request, "Amministrazione/Protocollo/UpdateProtocol.html",{'form': formProtocolUpdate(instance=Protocollo.objects.get(id=id))})
        else:
            anno != anno_pre and CalendarioContatore.objects.filter(id=anno).update(
                count=progressive_number_calendar + 1)
            messages.error(request, 'ATTENZIONE! La Data di Scadenza e la Data di Consegna devono essere necessariamente successive o uguali alla Data di Registrazione.')
            return render(request, "Amministrazione/Protocollo/UpdateProtocol.html", {'form': form})
    else:
        return render(request, "Amministrazione/Protocollo/UpdateProtocol.html", {'form': formProtocolUpdate(instance=Protocollo.objects.get(id=id))})

@login_required
def viewAllConsulenze(request):
    consulenza_filter = ConsulenzaFilter(request.GET, queryset=Consulenza.objects.all().order_by("-id"))
    for cons in consulenza_filter.qs:
        data_scadenza = datetime.strptime(str(cons.data_scadenza), "%Y-%m-%d").date()
        if cons.data_consegna != None:
            cons.status = None
        else:
            cons.status = (data_scadenza - date.today()).days
            Consulenza.objects.filter(id=cons.id).update(status=cons.status)
    sum_compensi = round(consulenza_filter.qs.aggregate(Sum('compenso'))['compenso__sum'] or 0, 2)
    return render(request, "Amministrazione/Consulenza/AllConsulenze.html", {"filter": consulenza_filter, 'filter_queryset': list(consulenza_filter.qs), 'sum_c': sum_compensi})

@login_required
def viewCreateConsulenza(request):
    if (request.method == "POST"):
        form = formConsulenza(request.POST)
        data_scadenza = datetime.strptime(form['data_scadenza'].value(), "%Y-%m-%d").date()
        form.set_status(None if form['data_consegna'].value() != None else (data_scadenza - date.today()).days)
        if (form.check_date()):
            if (form.is_valid()):
                form.save()
                return redirect('AllConsulenze')
            else:
                return render(request, "Amministrazione/Consulenza/CreateConsulenza.html", {'form': form})
        else:
            messages.error(request, 'ATTENZIONE! La Data di Scadenza e la Data di Consegna devono essere necessariamente successive o uguali alla Data di Registrazione.')
            return render(request, "Amministrazione/Consulenza/CreateConsulenza.html", {'form': form})
    else:
        return render(request, "Amministrazione/Consulenza/CreateConsulenza.html", {'form': formConsulenza()})

@login_required
def viewDeleteConsulenza(request, id):
    Consulenza.objects.get(id=id).delete()
    return redirect('AllConsulenze')

@login_required
def viewDeleteConsulenzeGroup(request):
    if request.method == "POST":
        for task in request.POST.getlist('list[]'):
            Consulenza.objects.get(id=int(task)).delete()
    return render(request, "Homepage/HomePageAmministrazione.html")

@login_required
def viewUpdateConsulenza(request, id):
    if (request.method == "POST"):
        form = formConsulenzaUpdate(request.POST, instance=Consulenza.objects.get(id=id))
        data_scadenza = datetime.strptime(form['data_scadenza'].value(), "%Y-%m-%d").date()
        form.set_status(None if form['data_consegna'].value() != None else (data_scadenza - date.today()).days)
        if (form.check_date()):
            if (form.is_valid()):
                form.save()
                return redirect('AllConsulenze')
            else:
                return render(request, "Amministrazione/Consulenza/UpdateConsulenza.html", {'form': form})
        else:
            messages.error(request, 'ATTENZIONE! La Data di Scadenza e la Data di Consegna devono essere necessariamente successive o uguali alla Data di Registrazione.')
            return render(request, "Amministrazione/Consulenza/UpdateConsulenza.html", {'form': form})
    else:
        return render(request, "Amministrazione/Consulenza/UpdateConsulenza.html", {'form': formConsulenzaUpdate(instance=Consulenza.objects.get(id=id))})

@login_required
def viewAllRicavi(request):
    ricavo_filter = RicavoFilter(request.GET, queryset=Ricavo.objects.all().order_by("-data_registrazione"))
    sum_ricavi_for_proto = [(r1.id, r1.protocollo.parcella - sum(r2.importo for r2 in ricavo_filter.qs if r1.protocollo == r2.protocollo)) if r1.protocollo is not None
                            else (r1.id,0) for r1 in ricavo_filter.qs ]
    sum_ricavi = round(ricavo_filter.qs.aggregate(Sum('importo'))['importo__sum'] or 0, 2)
    return render(request, "Contabilita/Ricavo/AllRicavi.html", {"filter": ricavo_filter, "filter_queryset": list(ricavo_filter.qs), 'sum_r': sum_ricavi, 'info': zip(ricavo_filter.qs, sum_ricavi_for_proto)})

def validate_ricavo_coerenza(fattura, protocollo, ricavo_attuale=None):
    if fattura:
        fattura_protocollo = fattura.protocollo

        # Controllo 1
        if fattura_protocollo and protocollo and fattura_protocollo != protocollo:
            return f"ATTENZIONE! La Fattura {fattura} è assegnata al Protocollo {fattura_protocollo} mentre tu hai selezionato il Protocollo {protocollo} per il Ricavo in oggetto"

        # Controllo 2
        if not fattura_protocollo and protocollo:
            return f"ATTENZIONE! La fattura {fattura} non ha un protocollo assegnato, mentre tu stai associando il Protocollo {protocollo} al Ricavo in oggetto"

        # Controllo 3
        if fattura_protocollo and not protocollo:
            return f"ATTENZIONE! La fattura {fattura} è assegnata al Protocollo {fattura_protocollo}, ma tu non stai associando nessun Protocollo al Ricavo in oggetto"

    return None

@login_required
def viewCreateRicavo(request):
    if request.method == "POST":
        form = formRicavo(request.POST)
        if form.is_valid():
            fattura = form.cleaned_data.get("fattura")
            protocollo = form.cleaned_data.get("protocollo")

            # Controllo coerenza Ricavo-Fattura-Protocollo
            error_msg = validate_ricavo_coerenza(fattura, protocollo)
            if error_msg:
                messages.error(request, error_msg)
                return render(request, "Contabilita/Ricavo/CreateRicavo.html", {'form': form})

            # Controllo importo <= parcella
            if protocollo and not form.Check1():
                messages.error(request,
                               f"ATTENZIONE! L'importo inserito rende la somma dei ricavi del protocollo {protocollo} maggiore della sua parcella: {protocollo.parcella} €")
                return render(request, "Contabilita/Ricavo/CreateRicavo.html", {'form': form})

            # Controllo somma importi ricavi <= importo fattura
            if fattura:
                totale_ricavi_fattura = Ricavo.objects.filter(fattura=fattura).aggregate(Sum('importo'))['importo__sum'] or 0
                nuovo_importo = form.cleaned_data.get("importo")
                if totale_ricavi_fattura + nuovo_importo > fattura.importo:
                    messages.error(request,
                                   f"ATTENZIONE! L'importo inserito rende la somma dei ricavi {totale_ricavi_fattura + nuovo_importo} della fattura {fattura.identificativo} maggiore del suo importo: {fattura.importo} €")
                    return render(request, "Contabilita/Ricavo/CreateRicavo.html", {'form': form})

            form.save()
            return redirect('AllRicavi')
        else:
            return render(request, "Contabilita/Ricavo/CreateRicavo.html", {'form': form})
    else:
        return render(request, "Contabilita/Ricavo/CreateRicavo.html", {'form': formRicavo()})


@login_required
def viewDeleteRicavo(id):
    Ricavo.objects.get(id=id).delete()
    return redirect('AllRicavi')

@login_required
def viewDeleteRicaviGroup(request):
    if request.method == "POST":
        for task in request.POST.getlist('list[]'):
            Ricavo.objects.get(id=int(task)).delete()
    return render(request, "Homepage/HomePageContabilita.html")

@login_required
def viewUpdateRicavo(request, id):
    ricavo = Ricavo.objects.get(id=id)
    if request.method == "POST":
        form = formRicavoUpdate(request.POST, instance=ricavo)
        if form.is_valid():
            fattura = form.cleaned_data.get("fattura")
            protocollo = form.cleaned_data.get("protocollo")

            # Controllo coerenza
            error_msg = validate_ricavo_coerenza(fattura, protocollo, ricavo_attuale=ricavo)
            if error_msg:
                messages.error(request, error_msg)
                return render(request, "Contabilita/Ricavo/UpdateRicavo.html", {'form': form})

            # Controllo parcella
            if protocollo and not form.Check2(ricavo):
                messages.error(request,
                               f"ATTENZIONE! L'importo inserito rende la somma dei ricavi del protocollo {protocollo} maggiore della sua parcella: {protocollo.parcella} €" )
                return render(request, "Contabilita/Ricavo/UpdateRicavo.html", {'form': form})

            # Controllo importo > fattura (sommando i ricavi esistenti, ma sostituendo l'importo del ricavo attuale con quello nuovo)
            if fattura:
                nuovo_importo = form.cleaned_data.get("importo")
                # Somma di tutti i ricavi tranne quello attuale
                somma_altri_ricavi = Ricavo.objects.filter(fattura=fattura).exclude(id=ricavo.id).aggregate(Sum('importo'))['importo__sum'] or 0
                # Somma complessiva con il nuovo importo aggiornato
                somma_totale = somma_altri_ricavi + nuovo_importo
                if somma_totale > fattura.importo:
                    messages.error(request,
                                   f"ATTENZIONE! L'importo aggiornato rende la somma dei ricavi {somma_totale} della fattura {fattura.identificativo} maggiore del suo importo: {fattura.importo} €")
                    return render(request, "Contabilita/Ricavo/UpdateRicavo.html", {'form': form})

            form.save()
            return redirect('AllRicavi')
        else:
            return render(request, "Contabilita/Ricavo/UpdateRicavo.html", {'form': form})
    else:
        return render(request, "Contabilita/Ricavo/UpdateRicavo.html", {'form': formRicavoUpdate(instance=ricavo)})


@login_required
def viewAllSpeseCommessa(request):
    spesacommessa_filter = SpesaCommessaFilter(request.GET, queryset=SpesaCommessa.objects.all().order_by("-data_registrazione"))
    sum_spesecommessa = round(spesacommessa_filter.qs.aggregate(Sum('importo'))['importo__sum'] or 0, 2)
    return render(request, "Contabilita/SpesaCommessa/AllSpeseCommessa.html", {"filter": spesacommessa_filter, 'filter_queryset': list(spesacommessa_filter.qs), 'sum_s': sum_spesecommessa})

@login_required
def viewCreateSpesaCommessa(request):
    if (request.method == "POST"):
        form = formSpesaCommessa(request.POST)
        if (form.is_valid()):
            form.save()
            return redirect('AllSpeseCommessa')
        else:
            return render(request, "Contabilita/SpesaCommessa/CreateSpesaCommessa.html", {'form': form})
    else:
        return render(request, "Contabilita/SpesaCommessa/CreateSpesaCommessa.html", {'form': formSpesaCommessa()})

@login_required
def viewDeleteSpesaCommessa(id):
    SpesaCommessa.objects.get(id=id).delete()
    return redirect('AllSpeseCommessa')

@login_required
def viewDeleteSpeseCommessaGroup(request):
    if request.method == "POST":
        for task in request.POST.getlist('list[]'):
            SpesaCommessa.objects.get(id=int(task)).delete()
    return render(request, "Homepage/HomePageContabilita.html")

@login_required
def viewUpdateSpesaCommessa(request, id):
    if (request.method == "POST"):
        form = formSpesaCommessaUpdate(request.POST, instance=SpesaCommessa.objects.get(id=id))
        if (form.is_valid()):
            form.save()
            return redirect('AllSpeseCommessa')
        else:
            return render(request, "Contabilita/SpesaCommessa/UpdateSpesaCommessa.html", {'form': form})
    else:
        return render(request, "Contabilita/SpesaCommessa/UpdateSpesaCommessa.html", {'form': formSpesaCommessaUpdate(instance=SpesaCommessa.objects.get(id=id))})

@login_required
def viewAllSpeseGestione(request):
    spesagestione_filter = SpesaGestioneFilter(request.GET, queryset=SpesaGestione.objects.all().order_by("-data_registrazione"))
    sum_spesegestione = round(spesagestione_filter.qs.aggregate(Sum('importo'))['importo__sum'] or 0, 2)
    return render(request, "Contabilita/SpesaGestione/AllSpeseGestione.html", {"filter": spesagestione_filter, 'filter_queryset': list(spesagestione_filter.qs), 'sum_s': sum_spesegestione})

@login_required
def viewCreateSpesaGestione(request):
    if (request.method == "POST"):
        form = formSpesaGestione(request.POST)
        if (form.is_valid()):
            form.save()
            return redirect('AllSpeseGestione')
        else:
            return render(request, "Contabilita/SpesaGestione/CreateSpesaGestione.html", {'form': form})
    else:
        return render(request, "Contabilita/SpesaGestione/CreateSpesaGestione.html", {'form': formSpesaGestione()})

@login_required
def viewDeleteSpesaGestione(id):
    SpesaGestione.objects.get(id=id).delete()
    return redirect('AllSpeseGestione')

@login_required
def viewDeleteSpeseGestioneGroup(request):
    if request.method == "POST":
        for task in request.POST.getlist('list[]'):
            SpesaGestione.objects.get(id=int(task)).delete()
    return render(request, "Homepage/HomePageContabilita.html")

@login_required
def viewUpdateSpesaGestione(request, id):
    if (request.method == "POST"):
        form = formSpesaGestioneUpdate(request.POST, instance=SpesaGestione.objects.get(id=id))
        if (form.is_valid()):
            form.save()
            return redirect('AllSpeseGestione')
        else:
            return render(request, "Contabilita/SpesaGestione/UpdateSpesaGestione.html", {'form': form})
    else:
        return render(request, "Contabilita/SpesaGestione/UpdateSpesaGestione.html", {'form': formSpesaGestioneUpdate(instance=SpesaGestione.objects.get(id=id))})

@login_required
def viewAllFatture(request):
    fattura_filter = FatturaFilter(request.GET, queryset=Fattura.objects.all().order_by("-data_registrazione"))
    sum_fatture = round(fattura_filter.qs.aggregate(Sum('importo'))['importo__sum'] or 0, 2)
    return render(request, "Contabilita/Fattura/AllFatture.html",
                  {"filter": fattura_filter, 'filter_queryset': list(fattura_filter.qs), 'sum_f': sum_fatture})

@login_required
def viewCreateFattura(request):
    if (request.method == "POST"):
        form = formFattura(request.POST)
        anno = form['data_registrazione'].value()[0:4]
        progressive_number_calendar = CalendarioContatore.objects.filter(id=anno).values('fatture')[0]['fatture']
        CalendarioContatore.objects.filter(id=anno).update(fatture=progressive_number_calendar + 1)
        form.set_identificativo(str('FT_{0:02}'.format(progressive_number_calendar + 1)) + "-" + anno[2:4])
        form.calcola_importo(float(form['imponibile'].value()))
        if (form.is_valid()):
            protocollo = form.cleaned_data.get('protocollo')
            nuovo_importo = float(form.cleaned_data.get('importo') or 0)
            if protocollo:
                fatture_esistenti = Fattura.objects.filter(protocollo=protocollo)
                totale_fatture = sum(float(f.importo) or 0 for f in fatture_esistenti) + nuovo_importo
                if totale_fatture > float(protocollo.parcella):
                    messages.error(
                        request,
                        f"ATTENZIONE! La somma degli importi delle fatture ({totale_fatture:.2f} €) associate al Protocollo {protocollo.identificativo} supera il valore della sua parcella ({protocollo.parcella:.2f} €)"
                    )
                    CalendarioContatore.objects.filter(id=anno).update(fatture=progressive_number_calendar)
                    return render(request, "Contabilita/Fattura/CreateFattura.html", {'form': form})
            form.save()
            return redirect('AllFatture')
        else:
            CalendarioContatore.objects.filter(id=anno).update(fatture=progressive_number_calendar)
            return render(request, "Contabilita/Fattura/CreateFattura.html", {'form': form})
    else:
        return render(request, "Contabilita/Fattura/CreateFattura.html", {'form': formFattura()})

@login_required
def viewDeleteFattura(id):
    Fattura.objects.get(id=id).delete()
    return redirect('AllFatture')

@login_required
def viewDeleteFattureGroup(request):
    if request.method == "POST":
        for task in request.POST.getlist('list[]'):
            Fattura.objects.get(id=int(task)).delete()
    return render(request, "Homepage/HomePageContabilita.html")

@login_required
def viewUpdateFattura(request, id):
    fattura = Fattura.objects.get(id=id)
    old_protocollo = fattura.protocollo
    if (request.method == "POST"):
        form = formFatturaUpdate(request.POST, instance=fattura)
        anno = form['data_registrazione'].value()[:4]
        progressive_number_calendar = CalendarioContatore.objects.filter(id=anno).values('fatture')[0]['fatture']
        anno_pre = str(fattura.data_registrazione.year)
        if anno != anno_pre:
            CalendarioContatore.objects.filter(id=anno).update(fatture=progressive_number_calendar + 1)
            form.set_identificativo(str('FT_{0:02}'.format(progressive_number_calendar + 1)) + "-" + anno[2:4])
        form.calcola_importo(float(form['imponibile'].value()))
        if (form.is_valid()):
            nuovo_protocollo = form.cleaned_data['protocollo']
            nuovo_importo = float(form.cleaned_data.get('importo') or 0)
            ricavi = fattura.ricavi_fattura.all()  # Ricavi associati alla fattura
            if ricavi.exists():
                # Prendiamo il primo protocollo tra i ricavi
                protocollo_ricavi = ricavi.first().protocollo
                tutti_ricavi_stesso_protocollo = all(r.protocollo == protocollo_ricavi for r in ricavi)
                if not tutti_ricavi_stesso_protocollo:
                    messages.error(request, f"ATTENZIONE! I ricavi Associati alla fattura {fattura.identificativo} sono assegnati a protocolli differenti")
                    anno != anno_pre and CalendarioContatore.objects.filter(id=anno).update(
                        fatture=progressive_number_calendar + 1)
                    return render(request, "Contabilita/Fattura/UpdateFattura.html", {'form': form})
                if (old_protocollo == protocollo_ricavi) and protocollo_ricavi != nuovo_protocollo:
                    messages.error(
                        request,
                        f"ATTENZIONE! Alla fattura con identificativo: {fattura.identificativo} "
                        f"non può essere modificato il protocollo con il valore {nuovo_protocollo}, "
                        f"poiché i ricavi associati a questa fattura sono legati al protocollo {protocollo_ricavi}"
                    )
                    anno != anno_pre and CalendarioContatore.objects.filter(id=anno).update(
                        fatture=progressive_number_calendar + 1)
                    return render(request, "Contabilita/Fattura/UpdateFattura.html", {'form': form})

            if nuovo_protocollo:
                fatture_collegate = Fattura.objects.filter(protocollo=nuovo_protocollo).exclude(id=fattura.id)
                totale_fatture = sum(float(f.importo) or 0 for f in fatture_collegate) + nuovo_importo
                if totale_fatture > float(nuovo_protocollo.parcella):
                    messages.error(
                        request,
                        f"ATTENZIONE! La somma degli importi delle Fatture diventerebbe ({totale_fatture:.2f} €) superando la parcella ({nuovo_protocollo.parcella:.2f} €) del protocollo {nuovo_protocollo.identificativo}"
                    )
                    anno != anno_pre and CalendarioContatore.objects.filter(id=anno).update(
                        fatture=progressive_number_calendar + 1)
                    return render(request, "Contabilita/Fattura/UpdateFattura.html", {'form': form})

            somma_ricavi = ricavi.aggregate(Sum('importo'))['importo__sum'] or 0
            if somma_ricavi > nuovo_importo:
                messages.error(
                    request,
                    f"ATTENZIONE! La somma dei ricavi associati diventerebbe ({somma_ricavi:.2f} €) superando l'importo della fattura ({nuovo_importo:.2f} €)"
                )
                anno != anno_pre and CalendarioContatore.objects.filter(id=anno).update(
                    fatture=progressive_number_calendar + 1)
                return render(request, "Contabilita/Fattura/UpdateFattura.html", {'form': form})

            # Nessun ricavo associato o controlli superati
            form.save()
            anno != anno_pre and Fattura.objects.filter(id=id).update(
                identificativo=str('FT_{0:02}'.format(progressive_number_calendar + 1)) + "-" + anno[2:4])
            return redirect('AllFatture')
        else:
            anno != anno_pre and CalendarioContatore.objects.filter(id=anno).update(fatture=progressive_number_calendar + 1)
            return render(request, "Contabilita/Fattura/UpdateFattura.html", {'form': form})
    else:
        return render(request, "Contabilita/Fattura/UpdateFattura.html",
                  {'form': formFatturaUpdate(instance=fattura)})

@login_required
def viewResoconto(request):
    if (request.method == "POST"):
        form = form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(request.POST)
        if (form.is_valid()):
            risultato = sqlite.resoconto(
                form.cleaned_data['data_inizio'],
                form.cleaned_data['data_fine']
            )
            # Ordina per data (opzionale ma consigliato)
            ordinato = sorted(risultato, key=lambda x: x[0])
            labels = [row[0] for row in ordinato]
            serie1 = [row[1] for row in ordinato]  # Spese
            serie2 = [row[2] for row in ordinato]  # Ricavi
            serie3 = [row[3] for row in ordinato]  # Utile
            context = {
                'form': form,
                'tabella_output1': risultato,
                'data_inizio': form.cleaned_data['data_inizio'],
                'data_fine': form.cleaned_data['data_fine'],
                'labels': json.dumps(labels),
                'serie1': json.dumps(serie1),
                'serie2': json.dumps(serie2),
                'serie3': json.dumps(serie3),
            }
            return render(request, "Contabilita/Resoconto.html", context)
        else:
            context = {
                'form': form,
                'tabella_output1': [],
                'data_inizio': '',  # O None
                'data_fine': '',
                'labels': json.dumps([]),
                'serie1': json.dumps([]),
                'serie2': json.dumps([]),
                'serie3': json.dumps([]),
            }
            return render(request, "Contabilita/Resoconto.html", context)
    else:
        return render(request, "Contabilita/Resoconto.html", {'form': form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(), 'tabella_output1': []})

# def viewResocontoRicavi(request):
#     if not request.user.is_authenticated:
#         return redirect("/accounts/login/")
#     else:
#         if (request.method == "POST"):
#             form = form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(request.POST)
#             if (form.is_valid()):
#                 return render(request, "Contabilita/ResocontoRicavi.html", {'form': form, 'tabella_output2': sqlite.resoconto_ricavi(form['year'].value()), 'year': form['year'].value()})
#             else:
#                 return render(request, "Contabilita/ResocontoRicavi.html", {'form': form, 'tabella_output2': []})
#         else:
#             return render(request, "Contabilita/ResocontoRicavi.html", {'form': form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(), 'tabella_output2': []})

# def viewGestioneGuadagniEffettivi(request):
#     if not request.user.is_authenticated:
#         return redirect("/accounts/login/")
#     else:
#         if (request.method == "POST"):
#             form = form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(request.POST)
#             if (form.is_valid()):
#                 return render(request, "Contabilita/GestioneGuadagniEffettivi.html", {'form': form, 'tabella_output3': sqlite.resoconto_guadagni_effettivi(form['year'].value()), 'year': form['year'].value()})
#             else:
#                 return render(request, "Contabilita/GestioneGuadagniEffettivi.html", {'form': form, 'tabella_output3': []})
#         else:
#             return render(request, "Contabilita/GestioneGuadagniEffettivi.html", {'form': form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(), 'tabella_output3': []})

@login_required
def viewContabilitaProtocolli(request):
    filter = request.POST.get("filter")
    protocols = sqlite.resoconto_contabilita_protocolli(filter)
    return render(request, "Contabilita/ContabilitaProtocolli.html", {'tabella_output4': protocols, 'tot_saldo': sum([protocol[9] for protocol in protocols]), 'cliente_filter': filter if filter else ""})

def export_input_table_xls(request, list, model):
    fields_models = {'protocollo': ['Identificativo', 'Nominativo Cliente', 'Telefono Cliente', 'Nominativo Referente', 'Telefono Referente', 'Indirizzo', 'Pratica', 'Parcella', 'Note', 'Data Registrazione', 'Data Consegna'],
                     'ricavo': ['Data Registrazione', 'Movimento', 'Importo', 'Id Fattura', 'Id Protocollo', 'Indirizzo Protocollo', 'Note'],
                     'spesacommessa': ['Data Registrazione', 'Importo', 'Id Protocollo', 'Indirizzo Protocollo', 'Note'],
                     'spesagestione': ['Data Registrazione', 'Importo', 'Causale', 'Fattura'],
                     'consulenza': ['Data Registrazione', 'Richiedente', 'Indirizzo', 'Attivita', 'Compenso', 'Note', 'Data Scadenza', 'Data Consegna'],
                     'rubricaclienti': ['Nominativo', 'Telefono', 'Mail', 'Note'],
                     'rubricareferenti': ['Nominativo', 'Telefono', 'Mail', 'Note'],
                     'fattura': ['Identificativo', 'Data Registrazione', 'Id Protocollo', 'Intestatario Protocollo', 'Indirizzo Protocollo', 'Importo']}
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}.xls"'.format(request.POST.get("fname"))
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(model)
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = fields_models[model]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    if model == 'protocollo':
        rows = Protocollo.objects.filter(identificativo__in=re.findall("(\d+-\d+)", list)).order_by('-identificativo').values_list('identificativo', 'cliente__nominativo', 'cliente__tel', 'referente__nominativo', 'referente__tel', 'indirizzo', 'pratica', 'parcella', 'note', 'data_registrazione', 'data_consegna')
    if model == 'ricavo':
        rows = Ricavo.objects.filter(id__in=re.findall("(\d+)", list)).order_by('-data_registrazione').values_list('data_registrazione', 'movimento', 'importo', 'fattura__identificativo', 'protocollo__identificativo', 'protocollo__indirizzo', 'note')
    if model == 'spesacommessa':
        rows = SpesaCommessa.objects.filter(id__in=re.findall("(\d+)", list)).order_by('-data_registrazione').values_list('data_registrazione', 'importo', 'protocollo__identificativo', 'protocollo__indirizzo', 'note')
    if model == 'spesagestione':
        rows = SpesaGestione.objects.filter(id__in=re.findall("(\d+)", list)).order_by('-data_registrazione').values_list('data_registrazione', 'importo', 'causale', 'fattura')
    if model == 'consulenza':
        rows = Consulenza.objects.filter(id__in=re.findall("(\d+)", list)).order_by('-data_registrazione').values_list('data_registrazione', 'richiedente', 'indirizzo', 'attivita', 'compenso', 'note', 'data_scadenza', 'data_consegna')
    if model == 'rubricaclienti':
        rows = RubricaClienti.objects.filter(tel__in=re.findall("(\d+)", list)).order_by('nominativo').values_list('nominativo', 'tel', 'mail', 'note')
    if model == 'rubricareferenti':
        rows = RubricaReferenti.objects.filter(tel__in=re.findall("(\d+)", list)).order_by('nominativo').values_list('nominativo', 'tel', 'mail', 'note')
    if model == 'fattura':
        rows = Fattura.objects.filter(identificativo__in=re.findall("(FT_\d+-\d+)", list)).order_by('-identificativo').values_list('identificativo', 'data_registrazione', 'protocollo__identificativo', 'protocollo__cliente__nominativo', 'protocollo__indirizzo', 'importo')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, re.sub(r'<[^<]+?>', '', str(row[col_num]).replace("None", '')), font_style)
    wb.save(response)
    return response

def export_output_table_xls(request, numquery, data_inizio, data_fine):
    output = ''
    if int(numquery) == 1:
        output = 'resoconto'
        columns = ['Mese - Anno', 'Spese di gestione (€)', 'Ricavi (€)', 'Utile (€)']
        rows = sqlite.resoconto(data_inizio, data_fine)
    # if int(numquery) == 2:
    #     output = 'ricavi'
    #     columns = ['Mese', 'Ricavi (€)', 'Daniele (€)', 'Laura (€)', 'Federico (€)']
    #     rows = sqlite.resoconto_ricavi(year)
    # if int(numquery) == 3:
    #     output = 'guadagni_eff'
    #     columns = ['Mese', 'Guadagni Teorici (€)', 'Guadagni Effettivi (€)', 'Daniele (€)', 'Laura (€)', 'Federico (€)', 'GT - GE (€)']
    #     rows = sqlite.resoconto_guadagni_effettivi(year)
    if int(numquery) == 4:
        output = 'contabilita_protocolli'
        columns = ['Id', 'Identificativo', 'Cliente', 'Referente', 'Indirizzo', 'Pratica', 'Parcella', 'Entrate', 'Uscite', 'Saldo']
        rows = sqlite.resoconto_contabilita_protocolli(request.POST.get("filter"))
    wb = xlwt.Workbook(encoding='utf-8')
    name_file = request.POST.get("fname")
    ws = wb.add_sheet(output)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}.xls"'.format(name_file)
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    for row in [dict(zip(columns, record)) for record in rows]:
        row_num += 1
        for col_num, key in enumerate(columns):
            value = row.get(key, '')
            ws.write(row_num, col_num, str(value).replace("None", ''), font_style)
    wb.save(response)
    return response