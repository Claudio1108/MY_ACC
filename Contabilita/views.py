import xlwt
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, ExpressionWrapper, DecimalField, Max, Q
from django.db.models.functions import Round, Coalesce
from .forms import *
from .filters import *
from datetime import date, datetime
from django.http import HttpResponse
from dal import autocomplete
from Contabilita import sqlite_queries as sqlite

class ProtocolloAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Protocollo.objects.all()
        if self.q:
            qs = qs.filter(
                Q(identificativo__icontains=self.q) | Q(indirizzo__icontains=self.q)
            )
        return qs.order_by("-data_registrazione__year", "-identificativo")

class FatturaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Fattura.objects.all().order_by('-identificativo')
        return qs.filter(identificativo__icontains=self.q) if self.q else qs

class F24Autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = F24.objects.all().order_by('-identificativo')
        return qs.filter(identificativo__icontains=self.q) if self.q else qs

class ClienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = RubricaClienti.objects.all().order_by('nominativo')
        return qs.filter(nominativo__icontains=self.q) | qs.filter(tel__icontains=self.q) if self.q else qs

class ReferenteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = RubricaReferenti.objects.all().order_by('nominativo')
        return qs.filter(nominativo__icontains=self.q) | qs.filter(tel__icontains=self.q) if self.q else qs

class ClienteReferenteAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        q = self.q or ""
        # Filtra e ordina i clienti per nominativo
        clienti = RubricaClienti.objects.filter(
            models.Q(nominativo__icontains=q) | models.Q(tel__icontains=q)
        ).order_by("nominativo")

        # Filtra e ordina i referenti per nominativo
        referenti = RubricaReferenti.objects.filter(
            models.Q(nominativo__icontains=q) | models.Q(tel__icontains=q)
        ).order_by("nominativo")

        risultati = []
        for c in clienti:
            risultati.append(f"[Cliente] {c.nominativo}")
        for r in referenti:
            risultati.append(f"[Referente] {r.nominativo}")
        return risultati

@login_required
def viewHomePage(request):
    return render(request, "Homepage/HomePage.html", {"user": request.user})

@login_required
def viewHomePageContabilita(request):
    return render(request, "Homepage/HomePageContabilita.html")

@login_required
def viewHomePageAmministrazione(request):
    clienti_attivi = RubricaClienti.objects.filter(
        protocollo__data_consegna__isnull=True
    ).distinct().count()
    referenti_attivi = RubricaReferenti.objects.filter(
        protocollo__data_consegna__isnull=True
    ).distinct().count()
    context = {
        'count_active_protocols': Protocollo.objects.filter(data_consegna__isnull=True).count(),
        'count_protocols': Protocollo.objects.count(),
        'count_active_clients': clienti_attivi,
        'count_active_referents': referenti_attivi,
        'count_active_consultancies': Consulenza.objects.filter(data_consegna__isnull=True).count(),
        'count_consultancies': Consulenza.objects.count(),
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
        nominativo = form['nominativo'].value()
        if (form.is_valid()):
            form.save()
            messages.success(request, f'Cliente con Nominativo "{nominativo}" creato con successo')
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
    return redirect('AllClienti')

@login_required
def viewUpdateCliente(request, id):
    if (request.method == "POST"):
        form = formCliente(request.POST, instance=RubricaClienti.objects.get(id=id))
        nominativo = form['nominativo'].value()
        if (form.is_valid()):
            form.save()
            messages.success(request, f'Cliente con Nominativo "{nominativo}" modificato con successo')
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
        nominativo = form['nominativo'].value()
        if (form.is_valid()):
            form.save()
            messages.success(request, f'Referente con Nominativo "{nominativo}" creato con successo')
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
    return redirect('AllReferenti')

@login_required
def viewUpdateReferente(request, id):
    if (request.method == "POST"):
        form = formReferente(request.POST, instance=RubricaReferenti.objects.get(id=id))
        nominativo = form['nominativo'].value()
        if (form.is_valid()):
            form.save()
            messages.success(request, f'Referente con Nominativo "{nominativo}" modificato con successo')
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
                messages.success(request, f"Protocollo con Identificativo \"{form['identificativo'].value()}\" creato con successo")
                return redirect('AllProtocols')
            else:
                messages.error(request, f"ATTENZIONE! {form.errors}")
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
    return redirect('AllProtocols')

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
                    messages.success(request,
                                     f"Protocollo con Identificativo \"{form['identificativo'].value()}\" modificato con successo")
                    return redirect('AllProtocols')
                else:
                    messages.error(request, f"ATTENZIONE! {form.errors}")
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
                messages.success(request, f'Consulenza creata con successo')
                return redirect('AllConsulenze')
            else:
                messages.error(request, f"ATTENZIONE! {form.errors}")
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
    return redirect('AllConsulenze')

@login_required
def viewUpdateConsulenza(request, id):
    if (request.method == "POST"):
        form = formConsulenzaUpdate(request.POST, instance=Consulenza.objects.get(id=id))
        data_scadenza = datetime.strptime(form['data_scadenza'].value(), "%Y-%m-%d").date()
        form.set_status(None if form['data_consegna'].value() != None else (data_scadenza - date.today()).days)
        if (form.check_date()):
            if (form.is_valid()):
                form.save()
                messages.success(request, f'Consulenza modificata con successo')
                return redirect('AllConsulenze')
            else:
                messages.error(request, f"ATTENZIONE! {form.errors}")
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
            messages.success(request, f'Ricavo creato con successo')
            return redirect('AllRicavi')
        else:
            messages.error(request, f"ATTENZIONE! {form.errors}")
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
    return redirect('AllRicavi')

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
            messages.success(request, f'Ricavo modificato con successo')
            return redirect('AllRicavi')
        else:
            messages.error(request, f"ATTENZIONE! {form.errors}")
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
            messages.success(request, f'Spesa di Commessa creata con successo')
            return redirect('AllSpeseCommessa')
        else:
            messages.error(request, f"ATTENZIONE! {form.errors}")
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
    return redirect('AllSpeseCommessa')

@login_required
def viewUpdateSpesaCommessa(request, id):
    if (request.method == "POST"):
        form = formSpesaCommessaUpdate(request.POST, instance=SpesaCommessa.objects.get(id=id))
        if (form.is_valid()):
            form.save()
            messages.success(request, f'Spesa di Commessa modificata con successo')
            return redirect('AllSpeseCommessa')
        else:
            messages.error(request, f"ATTENZIONE! {form.errors}")
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
            f24 = form.cleaned_data.get("f24")
            importo_spesa = form.cleaned_data.get("importo")
            if f24:
                # Calcolo somma debito - credito, trattando None come 0
                somma_codicetributo = round(CodiceTributo.objects.filter(f24=f24).annotate(
                    debito_val=Coalesce('debito', Decimal('0.00')),
                    credito_val=Coalesce('credito', Decimal('0.00')),
                    differenza=ExpressionWrapper(
                        F('debito_val') - F('credito_val'),
                        output_field=models.DecimalField()
                    )
                ).aggregate(
                    totale=Coalesce(Sum('differenza'), Decimal('0.00'))
                )['totale'], 2)

                if importo_spesa != somma_codicetributo:
                    messages.error(
                        request,
                        f"L'importo inserito non corrisponde alla somma degli importi dei codici tributo associati all' \"F24 - {f24.identificativo}\" pari a {somma_codicetributo} €"
                    )
                    return render(request, "Contabilita/SpesaGestione/CreateSpesaGestione.html", {'form': form})

            form.save()
            messages.success(request, f"Spesa di Gestione creata con successo")
            return redirect('AllSpeseGestione')
        else:
            messages.error(request,f"ATTENZIONE! {form.errors}")
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
    return redirect('AllSpeseGestione')

@login_required
def viewUpdateSpesaGestione(request, id):
    if (request.method == "POST"):
        form = formSpesaGestioneUpdate(request.POST, instance=SpesaGestione.objects.get(id=id))
        if (form.is_valid()):
            f24 = form.cleaned_data.get("f24")
            importo_spesa = form.cleaned_data.get("importo")
            if f24:
                # Calcolo somma debito - credito, trattando None come 0
                somma_codicetributo = round(CodiceTributo.objects.filter(f24=f24).annotate(
                    debito_val=Coalesce('debito', Decimal('0.00')),
                    credito_val=Coalesce('credito', Decimal('0.00')),
                    differenza=ExpressionWrapper(
                        F('debito_val') - F('credito_val'),
                        output_field=models.DecimalField()
                    )
                ).aggregate(
                    totale=Coalesce(Sum('differenza'), Decimal('0.00'))
                )['totale'], 2)

                if importo_spesa != somma_codicetributo:
                    messages.error(
                        request,
                        f"L'importo inserito non corrisponde alla somma degli importi dei codici tributo associati all' \"F24 - {f24.identificativo}\" pari a {somma_codicetributo} €"
                    )
                    return render(request, "Contabilita/SpesaGestione/CreateSpesaGestione.html", {'form': form})
            form.save()
            messages.success(request, f"Spesa di Gestione modificata con successo")
            return redirect('AllSpeseGestione')
        else:
            messages.error(request,f"ATTENZIONE! {form.errors}")
            return render(request, "Contabilita/SpesaGestione/UpdateSpesaGestione.html", {'form': form})
    else:
        return render(request, "Contabilita/SpesaGestione/UpdateSpesaGestione.html", {'form': formSpesaGestioneUpdate(instance=SpesaGestione.objects.get(id=id))})

@login_required
def viewAllFatture(request):
    fattura_filter = FatturaFilter(request.GET, queryset=Fattura.objects.all())
    fatture_ordinate = sorted(
        fattura_filter.qs,
        key=lambda f: tuple(
            int(x) if x.isdigit() else 0
            for x in re.match(r"FT_(\d+)-(\d+)", f.identificativo).groups()[::-1]
        ),
        reverse=True
    )
    sum_fatture = round(fattura_filter.qs.aggregate(Sum('importo'))['importo__sum'] or 0, 2)
    return render(request, "Contabilita/Fattura/AllFatture.html",
                  {"filter": fattura_filter, 'filter_queryset': fatture_ordinate, 'sum_f': sum_fatture})

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
            nuovo_imponibile = float(form.cleaned_data.get('imponibile') or 0)
            intestatario = form.cleaned_data.get('intestatario')
            if protocollo:
                fatture_esistenti = Fattura.objects.filter(protocollo=protocollo)
                totale_imponibile_fatture = sum(float(f.imponibile) or 0 for f in fatture_esistenti) + nuovo_imponibile
                if totale_imponibile_fatture > float(protocollo.parcella):
                    messages.error(
                        request,
                        f"ATTENZIONE! La somma degli imponibili delle fatture ({totale_imponibile_fatture:.2f} €) associate al Protocollo {protocollo.identificativo} supera il valore della sua parcella ({protocollo.parcella:.2f} €)"
                    )
                    CalendarioContatore.objects.filter(id=anno).update(fatture=progressive_number_calendar)
                    return render(request, "Contabilita/Fattura/CreateFattura.html", {'form': form})

                cliente_str = f"[Cliente] {protocollo.cliente.nominativo}"
                referente_str = f"[Referente] {protocollo.referente.nominativo}" if protocollo.referente else None
                if intestatario != cliente_str and intestatario != referente_str:
                    messages.error(
                        request,
                        f"ATTENZIONE! L'intestatario selezionato \"{intestatario}\" non corrisponde al Cliente e neanche al Referente associato al Protocollo \"{protocollo.identificativo}\"."
                    )
                    CalendarioContatore.objects.filter(id=anno).update(fatture=progressive_number_calendar)
                    return render(request, "Contabilita/Fattura/CreateFattura.html", {'form': form})

            form.save()
            messages.success(request, f"Fattura con Identificativo \"{form['identificativo'].value()}\" creata con successo")
            return redirect('AllFatture')
        else:
            CalendarioContatore.objects.filter(id=anno).update(fatture=progressive_number_calendar)
            messages.error(request, f"ATTENZIONE! {form.errors}")
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
    return redirect('AllFatture')

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
            nuovo_imponibile = float(form.cleaned_data.get('imponibile') or 0)
            intestatario = form.cleaned_data.get('intestatario')
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
                totale_imponibile_fatture = sum(float(f.imponibile) or 0 for f in fatture_collegate) + nuovo_imponibile
                if totale_imponibile_fatture > float(nuovo_protocollo.parcella):
                    messages.error(
                        request,
                        f"ATTENZIONE! La somma degli imponibili delle Fatture diventerebbe ({totale_imponibile_fatture:.2f} €) superando la parcella ({nuovo_protocollo.parcella:.2f} €) del protocollo {nuovo_protocollo.identificativo}"
                    )
                    anno != anno_pre and CalendarioContatore.objects.filter(id=anno).update(
                        fatture=progressive_number_calendar + 1)
                    return render(request, "Contabilita/Fattura/UpdateFattura.html", {'form': form})

                cliente_str = f"[Cliente] {nuovo_protocollo.cliente.nominativo}"
                referente_str = f"[Referente] {nuovo_protocollo.referente.nominativo}" if nuovo_protocollo.referente else None
                if intestatario != cliente_str and intestatario != referente_str:
                    messages.error(
                        request,
                        f"ATTENZIONE! L'intestatario selezionato \"{intestatario}\" non corrisponde al Cliente e neanche al Referente associato al Protocollo \"{nuovo_protocollo.identificativo}\"."
                    )
                    CalendarioContatore.objects.filter(id=anno).update(fatture=progressive_number_calendar)
                    return render(request, "Contabilita/Fattura/CreateFattura.html", {'form': formFatturaUpdate(instance=fattura)})

            somma_ricavi = ricavi.aggregate(Sum('importo'))['importo__sum'] or 0
            if somma_ricavi > nuovo_imponibile:
                messages.error(
                    request,
                    f"ATTENZIONE! La somma dei ricavi associati diventerebbe ({somma_ricavi:.2f} €) superando l'imponibile della fattura ({nuovo_imponibile:.2f} €)"
                )
                anno != anno_pre and CalendarioContatore.objects.filter(id=anno).update(
                    fatture=progressive_number_calendar + 1)
                return render(request, "Contabilita/Fattura/UpdateFattura.html", {'form': form})

            obj = form.save(commit=False)
            obj.intestatario = form.cleaned_data['intestatario']
            obj.save()
            anno != anno_pre and Fattura.objects.filter(id=id).update(
                identificativo=str('FT_{0:02}'.format(progressive_number_calendar + 1)) + "-" + anno[2:4])
            messages.success(request,
                             f"Fattura con Identificativo \"{form['identificativo'].value()}\" modificata con successo")
            return redirect('AllFatture')
        else:
            anno != anno_pre and CalendarioContatore.objects.filter(id=anno).update(fatture=progressive_number_calendar + 1)
            messages.error(request, f"ATTENZIONE! {form.errors}")
            return render(request, "Contabilita/Fattura/UpdateFattura.html", {'form': form})
    else:
        form = formFatturaUpdate(instance=fattura)
        return render(request, "Contabilita/Fattura/UpdateFattura.html",
                  {'form': form})

@login_required
def viewCreateCodiceTributo(request, f24_id):
    f24 = F24.objects.get(id=f24_id)
    if request.method == "POST":
        form = formCodiceTributo(request.POST)
        if form.is_valid():
            codice = form.save(commit=False)
            codice.f24 = f24
            codice.save()
            messages.success(request, f"Codice Tributo con Identificativo \"{codice.identificativo}\" creato con successo per l' \"{f24}\"")
            return redirect(f'/F24Detail/{f24.id}')
    else:
        form = formCodiceTributo(initial={'f24': f24})

    return render(request, "Contabilita/CodiceTributo/CreateCodiceTributo.html", {
        'form': form,
        'f24': f24,
    })

@login_required
def viewDeleteCodiciTributoGroup(request, f24_id):
    f24 = F24.objects.get(id=f24_id)
    if request.method == "POST":
        for task in request.POST.getlist('list[]'):
            CodiceTributo.objects.get(id=int(task)).delete()
    return redirect(f'/F24Detail/{f24.id}')

@login_required
def viewUpdateCodiceTributo(request, id, f24_id):
    codice = CodiceTributo.objects.get(id=id)
    f24 = F24.objects.get(id=f24_id)
    if request.method == "POST":
        post_data = request.POST.copy()
        post_data['f24'] = f24_id
        post_data['identificativo'] = codice.identificativo
        form = formCodiceTributoUpdate(post_data, instance=codice)
        if form.is_valid():
            identificativo = form.cleaned_data['identificativo']
            form.save()
            messages.success(request, f"Codice Tributo con Identificativo \"{identificativo}\" modificato con successo per l' \"{f24}\"")
            return redirect(f'/F24Detail/{f24.id}')
    else:
        form = formCodiceTributoUpdate(instance=codice)
        return render(request, "Contabilita/CodiceTributo/UpdateCodiceTributo.html", {
            'form': form,
            'f24': f24,
            'codice': codice,
        })

@login_required
def viewAllF24(request):
    f24_filter = F24Filter(request.GET, queryset=F24.objects.all().order_by("-identificativo"))
    filter_queryset = list(f24_filter.qs)

    somma_diff_per_f24 = []
    for f24 in filter_queryset:
        codici = f24.codicetributo.all()
        totale = sum((ct.debito or 0) - (ct.credito or 0) for ct in codici)
        somma_diff_per_f24.append(totale)

    f24_with_totals = list(zip(filter_queryset, somma_diff_per_f24))

    return render(
        request,
        "Contabilita/F24/AllF24.html",
        {
            "filter": f24_filter,
            "f24_with_totals": f24_with_totals  # nuova variabile da usare nel template
        }
    )

@login_required
def viewCreateF24(request):
    if (request.method == "POST"):
        form = formF24(request.POST)
        identificativo = form['identificativo'].value()
        if F24.objects.filter(identificativo=identificativo).exists():
        # if F24.objects.filter(identificativo__iexact=identificativo).exists():
            messages.error(request, f"ATTENZIONE! Esiste già un F24 con Identificativo \"{identificativo}\"")
            return render(request, "Contabilita/F24/CreateF24.html", {'form': form})
        if (form.is_valid()):
            form.save()
            messages.success(request, f"F24 con Identificativo \"{identificativo}\" creato con successo")
            return redirect('AllF24')
        else:
            messages.error(request, f"ATTENZIONE! {form.errors}")
            return render(request, "Contabilita/F24/CreateF24.html", {'form': form})
    else:
        return render(request, "Contabilita/F24/CreateF24.html", {'form': formF24()})

@login_required
def viewDeleteF24(id):
    F24.objects.get(id=id).delete()
    return redirect('AllF24')

@login_required
def viewDeleteF24Group(request):
    if request.method == "POST":
        for task in request.POST.getlist('list[]'):
            F24.objects.get(id=int(task)).delete()
    return redirect('AllF24')

@login_required
def viewUpdateF24(request, id):
    if (request.method == "POST"):
        form = formF24Update(request.POST, instance=F24.objects.get(id=id))
        identificativo = form['identificativo'].value()
        if (form.is_valid()):
            form.save()
            messages.success(request, f"F24 con Identificativo \"{identificativo}\" modificato con successo")
            return redirect('AllF24')
        else:
            messages.error(request, f"ATTENZIONE! {form.errors}")
            return render(request, "Contabilita/F24/UpdateF24.html", {'form': form})
    else:
        return render(request, "Contabilita/F24/UpdateF24.html",
                      {'form': formF24Update(instance=F24.objects.get(id=id))})

@login_required
def viewF24Detail(request, id):
    f_24 = F24.objects.get(id=id)
    codici_tributo_filter = CodiceTributoFilter(request.GET, queryset=CodiceTributo.objects.filter(f24=id).order_by("-anno"))
    codici = f_24.codicetributo.all()
    totale = sum((ct.debito or 0) - (ct.credito or 0) for ct in codici)
    return render(request, "Contabilita/F24/F24Detail.html",
                  {"codice_f24": str(f_24).replace("F24 -", ""), "data_scadenza_f24": f_24.data_scadenza, "f24_id": f_24.id,
                           "filter_queryset": list(codici_tributo_filter.qs), "ente": f_24.ente, "importo": totale})

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

@login_required
def viewResocontoFiscale(request):
    total = sqlite.resoconto_fiscale()
    return render(request, "Contabilita/ResocontoFiscale/ResocontoFiscale.html",{'tabella_output4': total})

@login_required
def viewResocontoFiscaleAnnuo(request, anno):
    imponibile = round(Fattura.objects.filter(data_registrazione__year=anno).aggregate(somma=Sum('imponibile'))['somma'] or Decimal('0.00'), 2)
    contributo_inarcassa = round(imponibile * Decimal('0.04'), 2)
    fatturato = imponibile + contributo_inarcassa
    importi_codicetributo_ade = CodiceTributo.objects.filter(
        anno=anno,
        f24__ente='AdE'
    ).annotate(
        importo=ExpressionWrapper(
            F('debito') - F('credito'),
            output_field=DecimalField(max_digits=14, decimal_places=2)
        )
    ).aggregate(
        totale=Sum('importo')
    )
    importo_ade = importi_codicetributo_ade['totale'] or Decimal('0.00')
    percentuale_importo_ade_su_fatturato =  round(importo_ade / fatturato * 100, 2) if fatturato != 0 else None
    importi_codicetributo_inarcassa = CodiceTributo.objects.filter(
        anno=anno,
        f24__ente='INARCASSA'
    ).annotate(
        importo=ExpressionWrapper(
            F('debito') - F('credito'),
            output_field=DecimalField(max_digits=14, decimal_places=2)
        )
    ).aggregate(
        totale=Sum('importo')
    )
    importo_inarcassa = round(importi_codicetributo_inarcassa.get('totale') or Decimal('0.00'), 2)
    percentuale_importo_inarcassa_su_fatturato = round(importo_inarcassa / fatturato * 100, 2) if fatturato != 0 else None
    importo_totale = importo_ade + importo_inarcassa
    percentuale_importo_totale_su_fatturato = round(importo_totale / fatturato * 100, 2) if fatturato != 0 else None
    percentuale =  round((importo_totale - contributo_inarcassa) / imponibile * 100, 2) if imponibile != 0 else None
    return render(request, "Contabilita/ResocontoFiscale/ResocontoFiscaleAnnuo.html",
                  {'anno': anno, 'imponibile': imponibile, 'contributo_inarcassa': contributo_inarcassa,
                   'fatturato': fatturato, 'importo_ade': importo_ade, 'importo_ade_su_fatturato': percentuale_importo_ade_su_fatturato,
                   'importo_inarcassa': importo_inarcassa, 'importo_inarcassa_su_fatturato': percentuale_importo_inarcassa_su_fatturato,
                   'importo_totale': importo_totale, 'importo_totale_su_fatturato': percentuale_importo_totale_su_fatturato,
                   'percentuale': percentuale})

@login_required
def viewResocontoFiscaleAnnuoFatture(request, anno):
    fatture = (
        Fattura.objects
        .filter(data_registrazione__year=anno)
        .annotate(
            contributo_inarcassa=
                ExpressionWrapper(
                    F('imponibile') * Decimal('0.04'),
                    output_field=DecimalField(max_digits=14, decimal_places=2)
            ),
            data_pagamento=Max('ricavi_fattura__data_registrazione')
        )
        .values(
            'identificativo',
            'intestatario',
            'imponibile',
            'contributo_inarcassa',
            'data_pagamento',
            'id'
        )
    )
    fatture_ordinate = sorted(
        fatture,
        key=lambda f: tuple(
            int(x) if x.isdigit() else 0
            for x in re.match(r"FT_(\d+)-(\d+)", f['identificativo']).groups()[::-1]
        ),
        reverse=True
    )
    return render(request, "Contabilita/ResocontoFiscale/ResocontoFiscaleAnnuoFatture.html",{'anno': anno, 'fatture': fatture_ordinate})

@login_required
def viewResocontoFiscaleAnnuoTasse(request, anno):
    codici = (
        CodiceTributo.objects
        .filter(anno=anno)
        .annotate(
            importo=ExpressionWrapper(
                Coalesce(F('debito'), 0) - Coalesce(F('credito'), 0),
                output_field=DecimalField(max_digits=14, decimal_places=2)
            ),
            identificativo_f24=F('f24__identificativo'),
            ente=F('f24__ente'),
            data_pagamento=F('f24__spesagestione__data_registrazione'),
            id_f24=F('f24__id')  # <-- ID dell'F24
        )
        .values(
            'id',  # ID del CodiceTributo
            'identificativo',
            'anno',
            'importo',
            'identificativo_f24',
            'id_f24',
            'ente',
            'data_pagamento'
        )
        .order_by('f24__data_scadenza', 'identificativo')
    )
    return render(request, "Contabilita/ResocontoFiscale/ResocontoFiscaleAnnuoTasse.html", {'anno': anno, 'codici': codici})

@login_required
def viewContabilitaProtocolli(request):
    filter = request.POST.get("filter")
    protocols = sqlite.resoconto_contabilita_protocolli(filter)
    protocols_ordered = sorted(
        protocols,
        key=lambda x: tuple(map(int, x[1].split('-')))[::-1],
        reverse=True
    )
    return render(request, "Contabilita/ContabilitaProtocolli.html", {'tabella_output4': protocols_ordered, 'tot_saldo': sum([protocol[9] for protocol in protocols_ordered]), 'cliente_filter': filter if filter else ""})

def export_input_table_xls(request, list, model):
    fields_models = {'protocollo': ['Identificativo', 'Nominativo Cliente', 'Telefono Cliente', 'Nominativo Referente', 'Telefono Referente', 'Indirizzo', 'Pratica', 'Parcella', 'Note', 'Data Registrazione', 'Data Consegna'],
                     'ricavo': ['Data Registrazione', 'Movimento', 'Importo', 'Id Fattura', 'Id Protocollo', 'Indirizzo Protocollo', 'Note'],
                     'spesacommessa': ['Data Registrazione', 'Importo', 'Id Protocollo', 'Indirizzo Protocollo', 'Note'],
                     'spesagestione': ['Identificativo', 'Data Registrazione', 'Importo', 'Causale', 'Fattura'],
                     'consulenza': ['Data Registrazione', 'Richiedente', 'Indirizzo', 'Attivita', 'Compenso', 'Note', 'Data Scadenza', 'Data Consegna'],
                     'rubricaclienti': ['Nominativo', 'Telefono', 'Mail', 'Note'],
                     'rubricareferenti': ['Nominativo', 'Telefono', 'Mail', 'Note'],
                     'fattura': ['Identificativo', 'Data Registrazione', 'Id Protocollo', 'Intestatario', 'Indirizzo Protocollo', 'Importo'],
                     'codicetributo': ['Identificativo', 'Anno', 'Mese', 'Debito', 'Credito'],
                     'f24': ['Identificativo', 'Data Scadenza', 'Ente']}
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
       # TODO F24 or Causale
        rows = SpesaGestione.objects.filter(identificativo__in=re.findall("(\d+)", list)).order_by('-identificativo').values_list('identificativo', 'data_registrazione', 'importo', 'causale', 'fattura')
    if model == 'consulenza':
        rows = Consulenza.objects.filter(id__in=re.findall("(\d+)", list)).order_by('-data_registrazione').values_list('data_registrazione', 'richiedente', 'indirizzo', 'attivita', 'compenso', 'note', 'data_scadenza', 'data_consegna')
    if model == 'rubricaclienti':
        rows = RubricaClienti.objects.filter(tel__in=re.findall("(\d+)", list)).order_by('nominativo').values_list('nominativo', 'tel', 'mail', 'note')
    if model == 'rubricareferenti':
        rows = RubricaReferenti.objects.filter(tel__in=re.findall("(\d+)", list)).order_by('nominativo').values_list('nominativo', 'tel', 'mail', 'note')
    if model == 'fattura':
        unordered_rows = Fattura.objects.filter(
            identificativo__in=re.findall(r"FT_\d+-\d+", list)
        ).values_list(
            'identificativo', 'data_registrazione', 'protocollo__identificativo',
            'intestatario', 'protocollo__indirizzo', 'importo'
        )
        rows = sorted(
            unordered_rows,
            key=lambda r: (
                (lambda m: (int(m.group(2)), int(m.group(1))) if m else (0, 0))
                (re.match(r"FT_(\d+)-(\d+)", r[0]))  # r[0] = identificativo
            ),
            reverse=True
        )
    if model == 'codicetributo':
        rows = CodiceTributo.objects.filter(identificativo__in=re.findall("(\d+)", list)).order_by('-identificativo').values_list('identificativo', 'anno', 'mese', 'debito', 'credito')
    if model == 'f24':
        rows = F24.objects.filter(identificativo__in=re.findall("(\d+)", list)).order_by('-identificativo').values_list('identificativo', 'data_scadenza', 'ente')
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
    if int(numquery) == 2:
        output = 'ricavi'
        columns = ['Anno', 'Importo Fatturato', 'Tasse', 'Utile', '%']
        rows = sqlite.resoconto_fiscale()
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