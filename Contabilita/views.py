import xlwt
import json
from django.shortcuts import render, redirect
from django.contrib import messages
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

class ClienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = RubricaClienti.objects.all().order_by('nominativo')
        return qs.filter(nominativo__icontains=self.q) | qs.filter(tel__icontains=self.q) if self.q else qs

class ReferenteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = RubricaReferenti.objects.all().order_by('nominativo')
        return qs.filter(nominativo__icontains=self.q) | qs.filter(tel__icontains=self.q) if self.q else qs

def viewHomePage(request):
    if not request.user.is_authenticated:
        return redirect("accounts/login/")
    else:
        return render(request, "Homepage/HomePage.html", {"user": request.user})

def viewHomePageContabilita(request):
    if not request.user.is_authenticated:
        return redirect("accounts/login/")
    else:
        return render(request, "Homepage/HomePageContabilita.html")

def viewHomePageAmministrazione(request):
    if not request.user.is_authenticated:
        return redirect("accounts/login/")
    context = {
        'count_active_protocols': Protocollo.objects.filter(data_consegna__isnull=True).count(),
        'count_deactive_protocols': Protocollo.objects.filter(data_consegna__isnull=False).count(),
        'count_clients': RubricaClienti.objects.count(),
        'count_referents': RubricaReferenti.objects.count(),
        'count_active_consultancies': Consulenza.objects.filter(data_consegna__isnull=True).count(),
        'count_deactive_consultancies': Consulenza.objects.filter(data_consegna__isnull=False).count(),
    }
    return render(request, "Homepage/HomePageAmministrazione.html", context)

def viewAllClienti(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        cliente_filter = ClienteFilter(request.GET, queryset=RubricaClienti.objects.all().order_by("nominativo"))
        return render(request, "Amministrazione/Cliente/AllClienti.html", {"filter": cliente_filter, "filter_queryset": list(cliente_filter.qs)})

def viewCreateCliente(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            form = formCliente(request.POST)
            if (form.is_valid()):
                form.save()
                return redirect('AllClienti')
            else:
                return render(request, "Amministrazione/Cliente/CreateCliente.html", {'form': form})
        else:
            return render(request, "Amministrazione/Cliente/CreateCliente.html", {'form': formCliente()})

def viewDeleteCliente(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        RubricaClienti.objects.get(id=id).delete()
        return redirect('AllClienti')

def viewDeleteClientiGroup(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            for task in request.POST.getlist('list[]'):
                RubricaClienti.objects.get(id=int(task)).delete()
        return render(request, "Homepage/HomePageAmministrazione.html")

def viewUpdateCliente(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            form = formCliente(request.POST, instance=RubricaClienti.objects.get(id=id))
            if (form.is_valid()):
                form.save()
                return redirect('AllClienti')
            else:
                return render(request, "Amministrazione/Cliente/UpdateCliente.html", {'form': form})
        else:
            return render(request, "Amministrazione/Cliente/UpdateCliente.html", {'form': formCliente(instance=RubricaClienti.objects.get(id=id))})

def viewAllReferenti(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        referente_filter = ReferenteFilter(request.GET, queryset=RubricaReferenti.objects.all().order_by("nominativo"))
        return render(request, "Amministrazione/Referente/AllReferenti.html",{"filter": referente_filter, "filter_queryset": list(referente_filter.qs)})

def viewCreateReferente(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            form = formReferente(request.POST)
            if (form.is_valid()):
                form.save()
                return redirect('AllReferenti')
            else:
                return render(request, "Amministrazione/Referente/CreateReferente.html", {'form': form})
        else:
            return render(request, "Amministrazione/Referente/CreateReferente.html", {'form': formReferente()})

def viewDeleteReferente(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        RubricaReferenti.objects.get(id=id).delete()
        return redirect('AllReferenti')

def viewDeleteReferentiGroup(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            for task in request.POST.getlist('list[]'):
                RubricaReferenti.objects.get(id=int(task)).delete()
        return render(request, "Homepage/HomePageAmministrazione.html")

def viewUpdateReferente(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            form = formReferente(request.POST, instance=RubricaReferenti.objects.get(id=id))
            if (form.is_valid()):
                form.save()
                return redirect('AllReferenti')
            else:
                return render(request, "Amministrazione/Referente/UpdateReferente.html", {'form': form})
        else:
            return render(request, "Amministrazione/Referente/UpdateReferente.html", {'form': formReferente(instance=RubricaReferenti.objects.get(id=id))})

def viewAllProtocols(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
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

def viewCreateProtocol(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            form = formProtocol(request.POST)
            anno = form['data_registrazione'].value()[0:4]
            progressive_number_calendar = CalendarioContatore.objects.filter(id=anno).values('count')[0]['count']
            CalendarioContatore.objects.filter(id=anno).update(count=str(progressive_number_calendar + 1))
            form.set_identificativo(str('{0:03}'.format(progressive_number_calendar + 1)) + "-" + anno[2:4])
            data_scadenza = datetime.strptime(form['data_scadenza'].value(), "%Y-%m-%d").date()
            form.set_status(None if form['data_consegna'].value() != None else (data_scadenza - date.today()).days)
            if (form.check_date()):
                if (form.is_valid()):
                    form.save()
                    return redirect('AllProtocols')
                else:
                    return render(request, "Amministrazione/Protocollo/CreateProtocol.html", {'form': form})
            else:
                messages.error(request, 'ATTENZIONE! La Data di Scadenza e la Data di Consegna devono essere necessariamente successive o uguali alla Data di Registrazione.')
                return render(request, "Amministrazione/Protocollo/CreateProtocol.html", {'form': form})
        else:
            return render(request, "Amministrazione/Protocollo/CreateProtocol.html", {'form': formProtocol()})

def viewDeleteProtocol(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        Protocollo.objects.get(id=id).delete()
        return redirect('AllProtocols')

def viewDeleteProtocolsGroup(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            for task in request.POST.getlist('list[]'):
                Protocollo.objects.get(id=int(task)).delete()
        return render(request, "Homepage/HomePageAmministrazione.html")

def viewUpdateProtocol(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            form = formProtocolUpdate(request.POST, instance=Protocollo.objects.get(id=id))
            anno = form['data_registrazione'].value()[:4]
            progressive_number_calendar = CalendarioContatore.objects.filter(id=anno).values('count')[0]['count']
            if anno != str(Protocollo.objects.get(id=id).data_registrazione.year):
                CalendarioContatore.objects.filter(id=anno).update(count=str(progressive_number_calendar + 1))
                form.set_identificativo(str('{0:03}'.format(progressive_number_calendar + 1)) + "-" + anno[2:4])
            data_scadenza = datetime.strptime(form['data_scadenza'].value(), "%Y-%m-%d").date()
            form.set_status(None if form['data_consegna'].value() != None else (data_scadenza - date.today()).days)
            if (form.check_date()):
                if form.check_ricavi_on_protocollo(id, form['parcella'].value()):
                    if (form.is_valid()):
                        form.save()
                        anno != str(Protocollo.objects.get(id=id).data_registrazione.year) and Protocollo.objects.filter(id=id).update(identificativo=str('{0:03}'.format(progressive_number_calendar + 1))+ "-" + anno[2:4])
                        return redirect('AllProtocols')
                    else:
                        return render(request, "Amministrazione/Protocollo/UpdateProtocol.html", {'form': form})
                else:
                    messages.error(request,
                                   f"ATTENZIONE! La somma degli importi dei ricavi associati al protocollo {form['identificativo'].value()} supera il valore della parcella inserito di {form['parcella'].value()}")
                    return render(request, "Amministrazione/Protocollo/UpdateProtocol.html",{'form': formProtocolUpdate(instance=Protocollo.objects.get(id=id))})
            else:
                messages.error(request, 'ATTENZIONE! La Data di Scadenza e la Data di Consegna devono essere necessariamente successive o uguali alla Data di Registrazione.')
                return render(request, "Amministrazione/Protocollo/UpdateProtocol.html", {'form': form})
        else:
            return render(request, "Amministrazione/Protocollo/UpdateProtocol.html", {'form': formProtocolUpdate(instance=Protocollo.objects.get(id=id))})

def viewAllConsulenze(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
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

def viewCreateConsulenza(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
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

def viewDeleteConsulenza(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        Consulenza.objects.get(id=id).delete()
        return redirect('AllConsulenze')

def viewDeleteConsulenzeGroup(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            for task in request.POST.getlist('list[]'):
                Consulenza.objects.get(id=int(task)).delete()
        return render(request, "Homepage/HomePageAmministrazione.html")

def viewUpdateConsulenza(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
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

def viewAllRicavi(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        ricavo_filter = RicavoFilter(request.GET, queryset=Ricavo.objects.all().order_by("-data_registrazione"))
        sum_ricavi_for_proto = [(r1.id, r1.protocollo.parcella - sum(r2.importo for r2 in ricavo_filter.qs if r1.protocollo == r2.protocollo)) if r1.protocollo is not None
                                else (r1.id,0) for r1 in ricavo_filter.qs ]
        sum_ricavi = round(ricavo_filter.qs.aggregate(Sum('importo'))['importo__sum'] or 0, 2)
        return render(request, "Contabilita/Ricavo/AllRicavi.html", {"filter": ricavo_filter, "filter_queryset": list(ricavo_filter.qs), 'sum_r': sum_ricavi, 'info': zip(ricavo_filter.qs, sum_ricavi_for_proto)})

def viewCreateRicavo(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            form = formRicavo(request.POST)
            if (form.is_valid()):
                if (form['protocollo'].value() != "" and not form.Check1()):
                    messages.error(request, 'ATTENZIONE! Il Ricavo inserito non rispetta i limiti di parcella del protocollo assegnato.')
                    return render(request, "Contabilita/Ricavo/CreateRicavo.html", {'form': form})
                else:
                    form.save()
                    return redirect('AllRicavi')
            else:
                return render(request, "Contabilita/Ricavo/CreateRicavo.html", {'form': form})
        else:
            return render(request, "Contabilita/Ricavo/CreateRicavo.html", {'form': formRicavo()})

def viewDeleteRicavo(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        Ricavo.objects.get(id=id).delete()
        return redirect('AllRicavi')

def viewDeleteRicaviGroup(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            for task in request.POST.getlist('list[]'):
                Ricavo.objects.get(id=int(task)).delete()
        return render(request, "Homepage/HomePageContabilita.html")

def viewUpdateRicavo(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            ricavo = Ricavo.objects.get(id=id)
            form = formRicavoUpdate(request.POST, instance=ricavo)
            if (form.is_valid()):
                if (form['protocollo'].value() != "" and not form.Check2(ricavo)):
                    messages.error(request, 'ATTENZIONE! Il Ricavo modificato non rispetta i limiti di parcella del protocollo assegnato.')
                    return render(request, "Contabilita/Ricavo/UpdateRicavo.html", {'form': form})
                else:
                    form.save()
                    return redirect('AllRicavi')
            else:
                return render(request, "Contabilita/Ricavo/UpdateRicavo.html", {'form': form})
        else:
            return render(request, "Contabilita/Ricavo/UpdateRicavo.html", {'form': formRicavoUpdate(instance=Ricavo.objects.get(id=id))})

def viewAllSpeseCommessa(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        spesacommessa_filter = SpesaCommessaFilter(request.GET, queryset=SpesaCommessa.objects.all().order_by("-data_registrazione"))
        sum_spesecommessa = round(spesacommessa_filter.qs.aggregate(Sum('importo'))['importo__sum'] or 0, 2)
        return render(request, "Contabilita/SpesaCommessa/AllSpeseCommessa.html", {"filter": spesacommessa_filter, 'filter_queryset': list(spesacommessa_filter.qs), 'sum_s': sum_spesecommessa})

def viewCreateSpesaCommessa(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            form = formSpesaCommessa(request.POST)
            if (form.is_valid()):
                form.save()
                return redirect('AllSpeseCommessa')
            else:
                return render(request, "Contabilita/SpesaCommessa/CreateSpesaCommessa.html", {'form': form})
        else:
            return render(request, "Contabilita/SpesaCommessa/CreateSpesaCommessa.html", {'form': formSpesaCommessa()})

def viewDeleteSpesaCommessa(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        SpesaCommessa.objects.get(id=id).delete()
        return redirect('AllSpeseCommessa')

def viewDeleteSpeseCommessaGroup(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            for task in request.POST.getlist('list[]'):
                SpesaCommessa.objects.get(id=int(task)).delete()
        return render(request, "Homepage/HomePageContabilita.html")

def viewUpdateSpesaCommessa(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            form = formSpesaCommessaUpdate(request.POST, instance=SpesaCommessa.objects.get(id=id))
            if (form.is_valid()):
                form.save()
                return redirect('AllSpeseCommessa')
            else:
                return render(request, "Contabilita/SpesaCommessa/UpdateSpesaCommessa.html", {'form': form})
        else:
            return render(request, "Contabilita/SpesaCommessa/UpdateSpesaCommessa.html", {'form': formSpesaCommessaUpdate(instance=SpesaCommessa.objects.get(id=id))})

def viewAllSpeseGestione(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        spesagestione_filter = SpesaGestioneFilter(request.GET, queryset=SpesaGestione.objects.all().order_by("-data_registrazione"))
        sum_spesegestione = round(spesagestione_filter.qs.aggregate(Sum('importo'))['importo__sum'] or 0, 2)
        return render(request, "Contabilita/SpesaGestione/AllSpeseGestione.html", {"filter": spesagestione_filter, 'filter_queryset': list(spesagestione_filter.qs), 'sum_s': sum_spesegestione})

def viewCreateSpesaGestione(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            form = formSpesaGestione(request.POST)
            if (form.is_valid()):
                form.save()
                return redirect('AllSpeseGestione')
            else:
                return render(request, "Contabilita/SpesaGestione/CreateSpesaGestione.html", {'form': form})
        else:
            return render(request, "Contabilita/SpesaGestione/CreateSpesaGestione.html", {'form': formSpesaGestione()})

def viewDeleteSpesaGestione(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        SpesaGestione.objects.get(id=id).delete()
        return redirect('AllSpeseGestione')

def viewDeleteSpeseGestioneGroup(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            for task in request.POST.getlist('list[]'):
                SpesaGestione.objects.get(id=int(task)).delete()
        return render(request, "Homepage/HomePageContabilita.html")

def viewUpdateSpesaGestione(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            form = formSpesaGestioneUpdate(request.POST, instance=SpesaGestione.objects.get(id=id))
            if (form.is_valid()):
                form.save()
                return redirect('AllSpeseGestione')
            else:
                return render(request, "Contabilita/SpesaGestione/UpdateSpesaGestione.html", {'form': form})
        else:
            return render(request, "Contabilita/SpesaGestione/UpdateSpesaGestione.html", {'form': formSpesaGestioneUpdate(instance=SpesaGestione.objects.get(id=id))})

def viewResoconto(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
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

def viewContabilitaProtocolli(request):
    filter = request.POST.get("filter")
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        protocols = sqlite.resoconto_contabilita_protocolli(filter)
        return render(request, "Contabilita/ContabilitaProtocolli.html", {'tabella_output4': protocols, 'tot_saldo': sum([protocol[9] for protocol in protocols]), 'cliente_filter': filter if filter else ""})

def export_input_table_xls(request, list, model):
    fields_models = {'protocollo': ['Identificativo', 'Nominativo Cliente', 'Telefono Cliente', 'Nominativo Referente', 'Telefono Referente', 'Indirizzo', 'Pratica', 'Parcella', 'Note', 'Data Registrazione', 'Data Consegna'],
                     'ricavo': ['Data Registrazione', 'Movimento', 'Importo', 'Fattura', 'Id Protocollo', 'Indirizzo Protocollo', 'Note'],
                     'spesacommessa': ['Data Registrazione', 'Importo', 'Id Protocollo', 'Indirizzo Protocollo', 'Note'],
                     'spesagestione': ['Data Registrazione', 'Importo', 'Causale', 'Fattura'],
                     'consulenza': ['Data Registrazione', 'Richiedente', 'Indirizzo', 'Attivita', 'Compenso', 'Note', 'Data Scadenza', 'Data Consegna'],
                     'rubricaclienti': ['Nominativo', 'Telefono', 'Mail', 'Note'],
                     'rubricareferenti': ['Nominativo', 'Telefono', 'Mail', 'Note']}
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
        rows = Ricavo.objects.filter(id__in=re.findall("(\d+)", list)).order_by('-data_registrazione').values_list('data_registrazione', 'movimento', 'importo', 'fattura', 'protocollo__identificativo', 'protocollo__indirizzo', 'note')
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