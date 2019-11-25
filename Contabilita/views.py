import re
import xlwt
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import *
from django.db import connection
from .filters import *
from datetime import date,datetime
from django.http import HttpResponse
from dal import autocomplete
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ProtocolloAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Protocollo.objects.all()
        if self.q:
            qs = qs.filter(identificativo__icontains=self.q) | qs.filter(indirizzo__icontains=self.q)
        return qs

class ClienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = RubricaClienti.objects.all()
        if self.q:
            qs = qs.filter(nominativo__icontains=self.q) | qs.filter(tel__icontains=self.q)
        return qs

class ReferenteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = RubricaReferenti.objects.all()
        if self.q:
            qs = qs.filter(nominativo__icontains=self.q) | qs.filter(tel__icontains=self.q)
        return qs

def viewHomePage(request):
    if not request.user.is_authenticated:
        return redirect("accounts/login/")
    else:
        return render(request, "Homepage/HomePage.html", {"user":request.user})

def viewHomePageContabilita(request):
    if not request.user.is_authenticated:
        return redirect("accounts/login/")
    else:
        return render(request, "Homepage/HomePageContabilita.html")

def viewHomePageAmministrazione(request):
    if not request.user.is_authenticated:
        return redirect("accounts/login/")
    else:
        return render(request, "Homepage/HomePageAmministrazione.html")

def viewAllClienti(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        clienti = RubricaClienti.objects.all()
        cliente_filter = ClienteFilter(request.GET, queryset=clienti.order_by("-nominativo"))
        # page = request.GET.get('page', 1)
        # paginator = Paginator(cliente_filter.qs, 20)
        # try:
        #     cl = paginator.page(page)
        # except PageNotAnInteger:
        #     cl = paginator.page(1)
        # except EmptyPage:
        #     cl = paginator.page(paginator.num_pages)
        # return render(request, "Amministrazione/Cliente/AllClienti.html", { "filter" : cliente_filter, 'cl': cl})
        return render(request, "Amministrazione/Cliente/AllClienti.html", {"filter":cliente_filter, "filter_queryset": cliente_filter.qs})

def viewCreateCliente(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if(request.method == "POST"):
            form = formCliente(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('AllClienti')
            else:
                return render(request, "Amministrazione/Cliente/CreateCliente.html", {'form': form})
        else:
            form = formCliente()
            return render(request,"Amministrazione/Cliente/CreateCliente.html",{'form':form})

def viewDeleteCliente(request,id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        cliente = RubricaClienti.objects.get(id=id)
        cliente.delete()
        return redirect('AllClienti')

def viewDeleteClientiGroup(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            tasks = request.POST.getlist('list[]')
            for task in tasks:
                cliente = RubricaClienti.objects.get(id=int(task))
                cliente.delete()
        return render(request, "Homepage/HomePageAmministrazione.html")

def viewUpdateCliente(request,id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            cliente = RubricaClienti.objects.get(id=id)
            form = formCliente(request.POST, instance=cliente)
            if (form.is_valid()):
                form.save()
                return redirect('AllClienti')
            else:
                return render(request, "Amministrazione/Cliente/UpdateCliente.html", {'form': form})
        else:
            cliente = RubricaClienti.objects.get(id=id)
            form = formCliente(instance=cliente)
            return render(request, "Amministrazione/Cliente/UpdateCliente.html", {'form': form})

def viewAllReferenti(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        referenti = RubricaReferenti.objects.all()
        referente_filter = ReferenteFilter(request.GET, queryset=referenti.order_by("-nominativo"))
        return render(request, "Amministrazione/Referente/AllReferenti.html", {"filter":referente_filter, "filter_queryset": referente_filter.qs})

def viewCreateReferente(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if(request.method == "POST"):
            form = formReferente(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('AllReferenti')
            else:
                return render(request, "Amministrazione/Referente/CreateReferente.html", {'form': form})
        else:
            form = formReferente()
            return render(request,"Amministrazione/Referente/CreateReferente.html",{'form':form})

def viewDeleteReferente(request,id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        referente = RubricaReferenti.objects.get(id=id)
        referente.delete()
        return redirect('AllReferenti')

def viewDeleteReferentiGroup(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            tasks = request.POST.getlist('list[]')
            for task in tasks:
                referente = RubricaReferenti.objects.get(id=int(task))
                referente.delete()
        return render(request, "Homepage/HomePageAmministrazione.html")

def viewUpdateReferente(request,id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            referente = RubricaReferenti.objects.get(id=id)
            form = formReferente(request.POST, instance=referente)
            if (form.is_valid()):
                form.save()
                return redirect('AllReferenti')
            else:
                return render(request, "Amministrazione/Referente/UpdateReferente.html", {'form': form})
        else:
            referente = RubricaReferenti.objects.get(id=id)
            form = formReferente(instance=referente)
            return render(request, "Amministrazione/Referente/UpdateReferente.html", {'form': form})

def viewAllProtocols(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        protocolli = Protocollo.objects.all()
        sum_parcelle = 0
        protocollo_filter = ProtocolloFilter(request.GET, queryset=protocolli.order_by("-identificativo"))
        today = date.today()
        for proto in protocollo_filter.qs:
            d = datetime.strptime(str(proto.data_scadenza), "%Y-%m-%d")
            data_scadenza = d.date()
            if proto.data_consegna != None:
                proto.status = None
            else:
                proto.status = (data_scadenza - today).days
                cursor = connection.cursor()
                cursor.execute("""update Contabilita_protocollo set status = {} where identificativo = '{}'""".format(proto.status,proto.identificativo))
            sum_parcelle=sum_parcelle+proto.parcella
        context = {"filter":protocollo_filter, 'filter_queryset': protocollo_filter.qs, 'sum_p': sum_parcelle}
        return render(request, "Amministrazione/Protocollo/AllProtocols.html", context)

def viewCreateProtocol(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if(request.method == "POST"):
            form = formProtocol(request.POST)
            anno=form['data_registrazione'].value()[0:4]
            cursor = connection.cursor()
            cursor.execute("""select count from Contabilita_calendariocontatore as c where c.id={}""".format(anno))
            rows = cursor.fetchone()
            val=rows[0]+1
            cursor = connection.cursor()
            cursor.execute("""update Contabilita_calendariocontatore  set count={} where id={}""".format(str(val),anno))
            form.set_identificativo(str('{0:03}'.format(val))+"-"+anno[2:4])
            today = date.today()
            d = datetime.strptime(form['data_scadenza'].value(), "%Y-%m-%d")
            data_scadenza = d.date()
            if form['data_consegna'].value() != '':
                form.set_status(0)
            else:
                form.set_status((data_scadenza - today).days)
            if(form.is_valid()):
                form.save()
                return redirect('AllProtocols')
            else:
                return render(request, "Amministrazione/Protocollo/CreateProtocol.html", {'form': form})
        else:
            form = formProtocol()
            return render(request,"Amministrazione/Protocollo/CreateProtocol.html", {'form':form})

def viewDeleteProtocol(request,id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        protocol = Protocollo.objects.get(id=id)
        protocol.delete()
        return redirect('AllProtocols')

def viewDeleteProtocolsGroup(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            tasks = request.POST.getlist('list[]')
            for task in tasks:
                protocol = Protocollo.objects.get(id=int(task))
                protocol.delete()
        return render(request, "Homepage/HomePageAmministrazione.html")

def viewUpdateProtocol(request,id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            protocol = Protocollo.objects.get(id=id)
            form = formProtocolUpdate(request.POST, instance=protocol)
            if (form.is_valid()):
                form.save()
                return redirect('AllProtocols')
            else:
                return render(request, "Amministrazione/Protocollo/UpdateProtocol.html", {'form': form})
        else:
            protocol = Protocollo.objects.get(id=id)
            form = formProtocolUpdate(instance=protocol)
            return render(request, "Amministrazione/Protocollo/UpdateProtocol.html", {'form': form})

def viewAllConsulenze(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        consulenze = Consulenza.objects.all()
        sum_compensi = 0
        consulenza_filter = ConsulenzaFilter(request.GET, queryset=consulenze.order_by("-id"))
        today = date.today()
        for cons in consulenza_filter.qs:
            d = datetime.strptime(str(cons.data_scadenza), "%Y-%m-%d")
            data_scadenza = d.date()
            if cons.data_consegna != None:
                cons.status = None
            else:
                cons.status = (data_scadenza - today).days
                cursor = connection.cursor()
                cursor.execute("""update Contabilita_consulenza set status = {} where id = '{}'""".format(cons.status,cons.id))
            sum_compensi=sum_compensi+cons.compenso
        context = {"filter":consulenza_filter, 'filter_queryset': consulenza_filter.qs, 'sum_c':sum_compensi}
        return render(request, "Amministrazione/Consulenza/AllConsulenze.html", context)

def viewCreateConsulenza(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if(request.method == "POST"):
            form = formConsulenza(request.POST)
            today = date.today()
            d = datetime.strptime(form['data_scadenza'].value(), "%Y-%m-%d")
            data_scadenza = d.date()
            if form['data_consegna'].value() != '':
                form.set_status(0)
            else:
                form.set_status((data_scadenza - today).days)

            if(form.is_valid()):
                form.save()
                return redirect('AllConsulenze')
            else:
                return render(request, "Amministrazione/Consulenza/CreateConsulenza.html", {'form': form})
        else:
            form = formConsulenza()
            return render(request,"Amministrazione/Consulenza/CreateConsulenza.html", {'form':form})

def viewDeleteConsulenza(request,id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        consulenza = Consulenza.objects.get(id=id)
        consulenza.delete()
        return redirect('AllConsulenze')

def viewDeleteConsulenzeGroup(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            tasks = request.POST.getlist('list[]')
            for task in tasks:
                consulenza = Consulenza.objects.get(id=int(task))
                consulenza.delete()
        return render(request, "Homepage/HomePageAmministrazione.html")

def viewUpdateConsulenza(request,id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            consulenza = Consulenza.objects.get(id=id)
            form = formConsulenzaUpdate(request.POST, instance=consulenza)
            if (form.is_valid()):
                form.save()
                return redirect('AllConsulenze')
            else:
                return render(request, "Amministrazione/Consulenza/UpdateConsulenza.html", {'form': form})
        else:
            consulenza = Consulenza.objects.get(id=id)
            form = formConsulenzaUpdate(instance=consulenza)
            return render(request, "Amministrazione/Consulenza/UpdateConsulenza.html", {'form': form})

def viewAllRicavi(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        ricavi = Ricavo.objects.all()
        ricavo_filter = RicavoFilter(request.GET, queryset=ricavi.order_by("-data_registrazione"))
        sum_ricavi = 0
        for ricavo in ricavo_filter.qs:
            sum_ricavi = sum_ricavi + ricavo.importo
        context = {"filter":ricavo_filter, 'filter_queryset': ricavo_filter.qs, 'sum_r':sum_ricavi}
        return render(request, "Contabilita/Ricavo/AllRicavi.html", context)

def viewCreateRicavo(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if(request.method == "POST"):
            form = formRicavo(request.POST)
            if(form.is_valid()):
                if(form['protocollo'].value()!=""):
                    if(form.Check1()):
                        form.save()
                    else:
                        messages.error(request, 'ATTENZIONE. Il Ricavo inserito non rispetta i vincoli di parcella del protocollo')
                    return redirect('AllRicavi')
                else:
                    form.save()
                    return redirect('AllRicavi')
            else:
                return render(request, "Contabilita/Ricavo/CreateRicavo.html", {'form': form})
        else:
            form = formRicavo()
            return render(request,"Contabilita/Ricavo/CreateRicavo.html",{'form':form})

def viewDeleteRicavo(request,id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        ricavo = Ricavo.objects.get(id=id)
        ricavo.delete()
        return redirect('AllRicavi')

def viewDeleteRicaviGroup(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            tasks = request.POST.getlist('list[]')
            for task in tasks:
                ricavo = Ricavo.objects.get(id=int(task))
                ricavo.delete()
        return render(request, "Homepage/HomePageContabilita.html")

def viewUpdateRicavo(request,id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            ricavo = Ricavo.objects.get(id=id)
            form = formRicavoUpdate(request.POST, instance=ricavo)
            if (form.is_valid()):
                if (form['protocollo'].value() != ""):
                    if (form.Check2(ricavo)):
                        form.save()
                    else:
                        messages.error(request,'ATTENZIONE. Il Ricavo inserito non rispetta i vincoli di parcella del protocollo')
                    return redirect('AllRicavi')
                else:
                    form.save()
                    return redirect('AllRicavi')
            else:
                return render(request, "Contabilita/Ricavo/UpdateRicavo.html", {'form': form})
        else:
            ricavo = Ricavo.objects.get(id=id)
            form = formRicavoUpdate(instance=ricavo)
            return render(request, "Contabilita/Ricavo/UpdateRicavo.html", {'form': form})

def viewAllSpeseCommessa(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        spesecommessa = SpesaCommessa.objects.all()
        spesacommessa_filter = SpesaCommessaFilter(request.GET, queryset=spesecommessa.order_by("-data_registrazione"))
        sum_spesecommessa = 0
        for s in spesacommessa_filter.qs:
            sum_spesecommessa = sum_spesecommessa + s.importo
        return render(request, "Contabilita/SpesaCommessa/AllSpeseCommessa.html", {"filter":spesacommessa_filter, 'filter_queryset': spesacommessa_filter.qs, 'sum_s': sum_spesecommessa})

def viewCreateSpesaCommessa(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if(request.method == "POST"):
            form = formSpesaCommessa(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('AllSpeseCommessa')
            else:
                return render(request, "Contabilita/SpesaCommessa/CreateSpesaCommessa.html", {'form': form})
        else:
            form = formSpesaCommessa()
            return render(request,"Contabilita/SpesaCommessa/CreateSpesaCommessa.html",{'form':form})

def viewDeleteSpesaCommessa(request,id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        spesacommessa = SpesaCommessa.objects.get(id=id)
        spesacommessa.delete()
        return redirect('AllSpeseCommessa')

def viewDeleteSpeseCommessaGroup(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            tasks = request.POST.getlist('list[]')
            for task in tasks:
                spesacommessa = SpesaCommessa.objects.get(id=int(task))
                spesacommessa.delete()
        return render(request, "Homepage/HomePageContabilita.html")

def viewUpdateSpesaCommessa(request,id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            spesacommessa = SpesaCommessa.objects.get(id=id)
            form = formSpesaCommessaUpdate(request.POST, instance=spesacommessa)
            if (form.is_valid()):
                form.save()
                return redirect('AllSpeseCommessa')
            else:
                return render(request, "Contabilita/SpesaCommessa/UpdateSpesaCommessa.html", {'form': form})
        else:
            spesacommessa = SpesaCommessa.objects.get(id=id)
            form = formSpesaCommessaUpdate(instance=spesacommessa)
            return render(request, "Contabilita/SpesaCommessa/UpdateSpesaCommessa.html", {'form': form})

def viewAllSoci(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        saldi=list()
        soci = Socio.objects.all().order_by("-percentuale")
        for tipo_saldo in ['CARTA', 'DEPOSITO']:
            query = """ SELECT coalesce(sum(t1.saldo),0)
                        FROM(
                        SELECT importo as saldo
                        FROM Contabilita_ricavo
                        WHERE destinazione='{t[tipo]}'
                        UNION
                        SELECT -importo as saldo
                        FROM Contabilita_spesagestione
                        WHERE provenienza='{t[tipo]}'
                        UNION
                        SELECT -importo as saldo
                        FROM Contabilita_spesacommessa
                        WHERE provenienza='{t[tipo]}'
                        UNION
                        SELECT -importo as saldo
                        FROM Contabilita_guadagnoeffettivo
                        WHERE provenienza='{t[tipo]}') t1""".format(t={'tipo': tipo_saldo})
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchone()
            saldi.append(rows[0])
        return render(request, "Contabilita/Socio/AllSoci.html", { "tabella_soci" : soci, "lista_saldi": saldi })

def viewUpdateSocio(request,id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            socio = Socio.objects.get(id=id)
            form = formSocio(request.POST, instance=socio)
            soci = Socio.objects.all()
            sum=0
            for soc in soci:
                if(soc.id != id):
                    sum+=soc.percentuale
            if (form.is_valid()):
                if(float(sum)+float(form['percentuale'].value()) < 1.00):
                    form.save()
                    messages.warning(request,'Le percentuali non sono distrubuite completamente')
                    return redirect('AllSoci')
                else:
                    if (float(sum) + float(form['percentuale'].value()) > 1.00):
                        messages.error(request,'ATTENZIONE. Percentuale inserita invalida')
                        return redirect('AllSoci')
                    else:
                        form.save()
                        return redirect('AllSoci')
            else:
                return render(request, "Contabilita/Socio/UpdateSocio.html", {'form': form, 'socio': socio})
        else:
            socio = Socio.objects.get(id=id)
            form = formSocio(instance=socio)
            return render(request, "Contabilita/Socio/UpdateSocio.html", {'form': form, 'socio':socio})

def viewAllSpeseGestione(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        spesegestione = SpesaGestione.objects.all()
        spesagestione_filter = SpesaGestioneFilter(request.GET, queryset=spesegestione.order_by("-data_registrazione"))
        sum_spesegestione = 0
        for s in spesagestione_filter.qs:
            sum_spesegestione = sum_spesegestione + s.importo
        return render(request, "Contabilita/SpesaGestione/AllSpeseGestione.html", {"filter":spesagestione_filter, 'filter_queryset': spesagestione_filter.qs, 'sum_s':sum_spesegestione})

def viewCreateSpesaGestione(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if(request.method == "POST"):
            form = formSpesaGestione(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('AllSpeseGestione')
            else:
                return render(request, "Contabilita/SpesaGestione/CreateSpesaGestione.html", {'form': form})
        else:
            form = formSpesaGestione()
            return render(request,"Contabilita/SpesaGestione/CreateSpesaGestione.html",{'form':form})

def viewDeleteSpesaGestione(request,id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        spesagestione = SpesaGestione.objects.get(id=id)
        spesagestione.delete()
        return redirect('AllSpeseGestione')

def viewDeleteSpeseGestioneGroup(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            tasks = request.POST.getlist('list[]')
            for task in tasks:
                spesagestione = SpesaGestione.objects.get(id=int(task))
                spesagestione.delete()
        return render(request, "Homepage/HomePageContabilita.html")

def viewUpdateSpesaGestione(request,id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            spesagestione = SpesaGestione.objects.get(id=id)
            form = formSpesaGestioneUpdate(request.POST, instance=spesagestione)
            if (form.is_valid()):
                form.save()
                return redirect('AllSpeseGestione')
            else:
                return render(request, "Contabilita/SpesaGestione/UpdateSpesaGestione.html", {'form': form})
        else:
            spesagestione = SpesaGestione.objects.get(id=id)
            form = formSpesaGestioneUpdate(instance=spesagestione)
            return render(request, "Contabilita/SpesaGestione/UpdateSpesaGestione.html", {'form': form})

def viewAllGuadagniEffettivi(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        guadagnieffettivi = GuadagnoEffettivo.objects.all()
        guadagnoeffettivo_filter = GuadagnoEffettivoFilter(request.GET, queryset=guadagnieffettivi.order_by("-data_registrazione"))
        sum_guadagnieffettivi = 0
        for g in guadagnoeffettivo_filter.qs:
            sum_guadagnieffettivi = sum_guadagnieffettivi + g.importo
        return render(request, "Contabilita/GuadagnoEffettivo/AllGuadagniEffettivi.html", {"filter":guadagnoeffettivo_filter, "filter_queryset" : guadagnoeffettivo_filter.qs, 'sum_g': sum_guadagnieffettivi})

def viewCreateGuadagnoEffettivo(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if(request.method == "POST"):
            form = formGuadagnoEffettivo(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('AllGuadagniEffettivi')
            else:
                return render(request, "Contabilita/GuadagnoEffettivo/CreateGuadagnoEffettivo.html", {'form': form})
        else:
            form = formGuadagnoEffettivo()
            return render(request,"Contabilita/GuadagnoEffettivo/CreateGuadagnoEffettivo.html",{'form':form})

def viewDeleteGuadagnoEffettivo(request,id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        guadagnoefettivo = GuadagnoEffettivo.objects.get(id=id)
        guadagnoefettivo.delete()
        return redirect('AllGuadagniEffettivi')

def viewDeleteGuadagniEffettiviGroup(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            tasks = request.POST.getlist('list[]')
            for task in tasks:
                guadagnoeffettivo = GuadagnoEffettivo.objects.get(id=int(task))
                guadagnoeffettivo.delete()
        return render(request, "Homepage/HomePageContabilita.html")

def viewUpdateGuadagnoEffettivo(request,id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            guadagnoeffettivo = GuadagnoEffettivo.objects.get(id=id)
            form = formGuadagnoEffettivoUpdate(request.POST, instance=guadagnoeffettivo)
            if (form.is_valid()):
                form.save()
                return redirect('AllGuadagniEffettivi')
            else:
                return render(request, "Contabilita/GuadagnoEffettivo/UpdateGuadagnoEffettivo.html", {'form': form})
        else:
            guadagnoeffettivo = GuadagnoEffettivo.objects.get(id=id)
            form = formGuadagnoEffettivoUpdate(instance=guadagnoeffettivo)
            return render(request, "Contabilita/GuadagnoEffettivo/UpdateGuadagnoEffettivo.html", {'form': form})

def execute_query_1(year):
    anno = str(year)
    query = """select '01/GENNAIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data_registrazione >= '{d[year]}-01-01' and t1.data_registrazione <= '{d[year]}-01-31' 
                        UNION
                        select '02/FEBBRAIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data_registrazione >= '{d[year]}-02-01' and t1.data_registrazione <= '{d[year]}-02-28' 
                        UNION
                        select '03/MARZO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data_registrazione >= '{d[year]}-03-01' and t1.data_registrazione <= '{d[year]}-03-31'
                        UNION
                        select '04/APRILE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data_registrazione >= '{d[year]}-04-01' and t1.data_registrazione <= '{d[year]}-04-30' 
                        UNION
                        select '05/MAGGIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data_registrazione >= '{d[year]}-05-01' and t1.data_registrazione <= '{d[year]}-05-31' 
                        UNION
                        select '06/GIUGNO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data_registrazione >= '{d[year]}-06-01' and t1.data_registrazione <= '{d[year]}-06-30' 
                        UNION
                        select '07/LUGLIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data_registrazione >= '{d[year]}-07-01' and t1.data_registrazione <= '{d[year]}-07-31' 
                        UNION
                        select '08/AGOSTO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data_registrazione >= '{d[year]}-08-01' and t1.data_registrazione <= '{d[year]}-08-31' 
                        UNION
                        select '09/SETTEMBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data_registrazione >= '{d[year]}-09-01' and t1.data_registrazione <= '{d[year]}-09-30' 
                        UNION
                        select '10/OTTOBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data_registrazione >= '{d[year]}-10-01' and t1.data_registrazione <= '{d[year]}-10-31' 
                        UNION
                        select '11/NOVEMBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data_registrazione >= '{d[year]}-11-01' and t1.data_registrazione <= '{d[year]}-11-30' 
                        UNION
                        select '12/DICEMBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data_registrazione >= '{d[year]}-12-01' and t1.data_registrazione <= '{d[year]}-12-31'
                        UNION
                        select 'TOTALE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1
                        where t1.data_registrazione >= '{d[year]}-01-01' and t1.data_registrazione <= '{d[year]}-12-31'
                        ORDER BY mese ASC;""".format(d={'year': anno})
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def viewResocontoSpeseGestione(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            form = form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(request.POST)
            if (form.is_valid()):
                return render(request, "Contabilita/ResocontoSpeseGestione.html", {'form': form, 'tabella_output1': execute_query_1(form['year'].value()), 'year': form['year'].value()})
            else:
                return render(request, "Contabilita/ResocontoSpeseGestione.html", {'form': form, 'tabella_output1': []})
        else:
            form = form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi()
            return render(request, "Contabilita/ResocontoSpeseGestione.html", {'form': form, 'tabella_output1':[]})

def execute_query_2(year):
    anno = str(year)
    query = """ select '01/GENNAIO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico
                from Contabilita_ricavo t1  
                where t1.data_registrazione >= '{d[year]}-01-01' and t1.data_registrazione <= '{d[year]}-01-31' 
                union
                select '02/FEBBRAIO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_ricavo t1  
                where t1.data_registrazione >= '{d[year]}-02-01' and t1.data_registrazione <= '{d[year]}-02-28' 
                union
                select '03/MARZO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_ricavo t1  
                where t1.data_registrazione >= '{d[year]}-03-01' and t1.data_registrazione <= '{d[year]}-03-31' 
                union
                select '04/APRILE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_ricavo t1
                where t1.data_registrazione >= '{d[year]}-04-01' and t1.data_registrazione <= '{d[year]}-04-30' 
                union
                select '05/MAGGIO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_ricavo t1
                where t1.data_registrazione >= '{d[year]}-05-01' and t1.data_registrazione <= '{d[year]}-05-31' 
                union
                select '06/GIUGNO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_ricavo t1
                where t1.data_registrazione >= '{d[year]}-06-01' and t1.data_registrazione <= '{d[year]}-06-30' 
                union
                select '07/LUGLIO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_ricavo t1
                where t1.data_registrazione >= '{d[year]}-07-01' and t1.data_registrazione <= '{d[year]}-07-31' 
                union
                select '08/AGOSTO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_ricavo t1
                where t1.data_registrazione >= '{d[year]}-08-01' and t1.data_registrazione <= '{d[year]}-08-31' 
                union
                select '09/SETTEMBRE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_ricavo t1
                where t1.data_registrazione >= '{d[year]}-09-01' and t1.data_registrazione <= '{d[year]}-09-30' 
                union
                select '10/OTTOBRE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_ricavo t1
                where t1.data_registrazione >= '{d[year]}-10-01' and t1.data_registrazione <= '{d[year]}-10-31' 
                union
                select '11/NOVEMBRE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_ricavo t1
                where t1.data_registrazione >= '{d[year]}-11-01' and t1.data_registrazione <= '{d[year]}-11-30' 
                union
                select '12/DICEMBRE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_ricavo t1
                where t1.data_registrazione >= '{d[year]}-12-01' and t1.data_registrazione <= '{d[year]}-12-31' 
                union
                select 'TOTALE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_ricavo t1
                where t1.data_registrazione >= '{d[year]}-01-01' and t1.data_registrazione <= '{d[year]}-12-31'
                ORDER BY mese ASC;""".format(d={'year': anno})
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def viewResocontoRicavi(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            form = form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(request.POST)
            if (form.is_valid()):
                return render(request, "Contabilita/ResocontoRicavi.html", {'form': form, 'tabella_output2': execute_query_2(form['year'].value()), 'year': form['year'].value()})
            else:
                return render(request, "Contabilita/ResocontoRicavi.html", {'form': form, 'tabella_output2': []})
        else:
            form = form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi()
            return render(request, "Contabilita/ResocontoRicavi.html", {'form': form, 'tabella_output2':[]})

def execute_query_3(year):
    anno = str(year)
    query = """select '01/GENNAIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-01-01' and t2.data_registrazione <= '{d[year]}-01-31') -
              (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-01-01' and t1.data_registrazione <= '{d[year]}-01-31') as GuadagniTeorici,
              coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
              (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-01-01' and t2.data_registrazione <= '{d[year]}-01-31') -
              (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-01-01' and t1.data_registrazione <= '{d[year]}-01-31')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1

            Where t1.data_registrazione >= '{d[year]}-01-01' and t1.data_registrazione <= '{d[year]}-01-31'
            union
            select '02/FEBBRAIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-02-01' and t2.data_registrazione <= '{d[year]}-02-28') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-02-01' and t1.data_registrazione <= '{d[year]}-02-28') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-02-01' and t2.data_registrazione <= '{d[year]}-02-28') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-02-01' and t1.data_registrazione <= '{d[year]}-02-28')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1
            Where t1.data_registrazione >= '{d[year]}-02-01' and t1.data_registrazione <= '{d[year]}-02-28'
            union
            select '03/MARZO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-03-01' and t2.data_registrazione <= '{d[year]}-03-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-03-01' and t1.data_registrazione <= '{d[year]}-03-31') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-03-01' and t2.data_registrazione <= '{d[year]}-03-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-03-01' and t1.data_registrazione <= '{d[year]}-03-31')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1
            Where t1.data_registrazione >= '{d[year]}-03-01' and t1.data_registrazione <= '{d[year]}-03-31'
            union
            select '04/APRILE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-04-01' and t2.data_registrazione <= '{d[year]}-04-30') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-04-01' and t1.data_registrazione <= '{d[year]}-04-30') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-04-01' and t2.data_registrazione <= '{d[year]}-04-30') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-04-01' and t1.data_registrazione <= '{d[year]}-04-30')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1

            Where t1.data_registrazione >= '{d[year]}-04-01' and t1.data_registrazione <= '{d[year]}-04-30'
            union
            select '05/MAGGIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-05-01' and t2.data_registrazione <= '{d[year]}-05-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-05-01' and t1.data_registrazione <= '{d[year]}-05-31') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-05-01' and t2.data_registrazione <= '{d[year]}-05-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-05-01' and t1.data_registrazione <= '{d[year]}-05-31')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1
            Where t1.data_registrazione >= '{d[year]}-05-01' and t1.data_registrazione <= '{d[year]}-05-31'
            union
            select '06/GIUGNO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-06-01' and t2.data_registrazione <= '{d[year]}-06-30') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-06-01' and t1.data_registrazione <= '{d[year]}-06-30') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-06-01' and t2.data_registrazione <= '{d[year]}-06-30') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-06-01' and t1.data_registrazione <= '{d[year]}-06-30')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1
            Where t1.data_registrazione >= '{d[year]}-06-01' and t1.data_registrazione <= '{d[year]}-06-30'
            union
            select '07/LUGLIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-07-01' and t2.data_registrazione <= '{d[year]}-07-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-07-01' and t1.data_registrazione <= '{d[year]}-07-31') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-07-01' and t2.data_registrazione <= '{d[year]}-07-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-07-01' and t1.data_registrazione <= '{d[year]}-07-31')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1
            Where t1.data_registrazione >= '{d[year]}-07-01' and t1.data_registrazione <= '{d[year]}-07-31'
            union
            select '08/AGOSTO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-08-01' and t2.data_registrazione <= '{d[year]}-08-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-08-01' and t1.data_registrazione <= '{d[year]}-08-31') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-08-01' and t2.data_registrazione <= '{d[year]}-08-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-08-01' and t1.data_registrazione <= '{d[year]}-08-31')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1
            Where t1.data_registrazione >= '{d[year]}-08-01' and t1.data_registrazione <= '{d[year]}-08-31'
            union
            select '09/SETTEMBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-09-01' and t2.data_registrazione <= '{d[year]}-09-30') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-09-01' and t1.data_registrazione <= '{d[year]}-09-30') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-09-01' and t2.data_registrazione <= '{d[year]}-09-30') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-09-01' and t1.data_registrazione <= '{d[year]}-09-30')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1
            Where t1.data_registrazione >= '{d[year]}-09-01' and t1.data_registrazione <= '{d[year]}-09-30'
            union
            select '10/OTTOBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-10-01' and t2.data_registrazione <= '{d[year]}-10-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-10-01' and t1.data_registrazione <= '{d[year]}-10-31') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-10-01' and t2.data_registrazione <= '{d[year]}-10-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-10-01' and t1.data_registrazione <= '{d[year]}-10-31')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1
            Where t1.data_registrazione >= '{d[year]}-10-01' and t1.data_registrazione <= '{d[year]}-10-31'
            union
            select '11/NOVEMBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-11-01' and t2.data_registrazione <= '{d[year]}-11-30') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-11-01' and t1.data_registrazione <= '{d[year]}-11-30') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-11-01' and t2.data_registrazione <= '{d[year]}-11-30') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-11-01' and t1.data_registrazione <= '{d[year]}-11-30')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1
            Where t1.data_registrazione >= '{d[year]}-11-01' and t1.data_registrazione <= '{d[year]}-11-30'
            union
            select '12/DICEMBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-12-01' and t2.data_registrazione <= '{d[year]}-12-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-12-01' and t1.data_registrazione <= '{d[year]}-12-31') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data_registrazione >= '{d[year]}-12-01' and t2.data_registrazione <= '{d[year]}-12-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data_registrazione >= '{d[year]}-12-01' and t1.data_registrazione <= '{d[year]}-12-31')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1
            Where t1.data_registrazione >= '2018-12-01' and t1.data_registrazione <= '2018-12-31'
            union
            select 'TOTALE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 Where t2.data_registrazione >= '{d[year]}-01-01' and t2.data_registrazione <= '{d[year]}-12-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 Where t1.data_registrazione >= '{d[year]}-01-01' and t1.data_registrazione <= '{d[year]}-12-31') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 Where t2.data_registrazione >= '{d[year]}-01-01' and t2.data_registrazione <= '{d[year]}-12-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 Where t1.data_registrazione >= '{d[year]}-01-01' and t1.data_registrazione <= '{d[year]}-12-31')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1
            Where t1.data_registrazione >= '{d[year]}-01-01' and t1.data_registrazione <= '{d[year]}-12-31'	  
            ORDER BY mese ASC;""".format(d={'year': anno})
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def viewGestioneGuadagniEffettivi(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if (request.method == "POST"):
            form = form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(request.POST)
            if (form.is_valid()):
                return render(request, "Contabilita/GestioneGuadagniEffettivi.html", {'form': form, 'tabella_output3': execute_query_3(form['year'].value()), 'year': form['year'].value()})
            else:
                return render(request, "Contabilita/GestioneGuadagniEffettivi.html", {'form': form, 'tabella_output3': []})
        else:
            form = form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi()
            return render(request, "Contabilita/GestioneGuadagniEffettivi.html", {'form': form, 'tabella_output3': []})

def execute_query_4():
    query = """SELECT t1.identificativo, t4.nominativo as cliente, t1.referente_id, t1.indirizzo,t1.pratica,t1.parcella,(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id) as entrate,
                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as uscite,
                            t1.parcella-(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id)+
                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as saldo
               FROM   Contabilita_protocollo t1, Contabilita_rubricaclienti t4
               WHERE saldo != 0 and t1.cliente_id = t4.id and t1.referente_id is NULL
               union
               SELECT t1.identificativo, t4.nominativo as cliente, t5.nominativo, t1.indirizzo,t1.pratica,t1.parcella,(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id) as entrate,
                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as uscite,
                            t1.parcella-(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id)+
                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as saldo
               FROM   Contabilita_protocollo t1, Contabilita_rubricaclienti t4, Contabilita_rubricareferenti t5
               WHERE saldo != 0 and t1.cliente_id = t4.id and t1.referente_id = t5.id"""
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def viewContabilitaProtocolli(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        return render(request, "Contabilita/ContabilitaProtocolli.html", {'tabella_output4': execute_query_4()})

def export_input_table_xls(request,list,model):
    fields_models = { 'protocollo': ['Identificativo', 'Data Registrazione', 'Nominativo Cliente', 'Telefono Cliente', 'Nominativo Referente', 'Telefono Referente', 'Indirizzo', 'Pratica', 'Parcella', 'Note', 'Data Scadenza', 'Data Consegna', 'Responsabile'],
                      'ricavo' : ['Data Registrazione','Movimento','Importo','Fattura','Intestatario Fattura','Id Protocollo', 'Indirizzo Protocollo', 'Note'],
                      'spesacommessa' : ['Data Registrazione','Importo','Id Protocollo', 'Indirizzo Protocollo', 'Note'],
                      'spesagestione' : ['Data Registrazione', 'Importo', 'Causale', 'Fattura'],
                      'guadagnoeffettivo' : ['Data Registrazione', 'Importo'],
                      'consulenza' : ['Data Registrazione', 'Richiedente', 'Indirizzo', 'Attivita', 'Compenso', 'Note', 'Data Scadenza', 'Data Consegna', 'Responsabile'],
                      'rubricaclienti' : ['Nominativo', 'Telefono', 'Mail', 'Note'],
                      'rubricareferenti' : ['Nominativo', 'Telefono', 'Mail', 'Note']}
    name_file = request.POST.get("fname")
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}.xls"'.format(name_file)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(model)
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = fields_models[model]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    if model == 'protocollo':
        rows = Protocollo.objects.filter(identificativo__in = re.findall("(\d+-\d+)",list)).values_list('identificativo', 'data_registrazione', 'cliente__nominativo', 'cliente__tel', 'referente__nominativo', 'referente__tel', 'indirizzo', 'pratica', 'parcella', 'note','data_scadenza' , 'data_consegna', 'responsabile__cognome')
    if model == 'ricavo':
        rows = Ricavo.objects.filter(id__in = re.findall("(\d+)",list)).values_list('data_registrazione', 'movimento', 'importo', 'fattura', 'intestatario_fattura__cognome', 'protocollo__identificativo', 'protocollo__indirizzo', 'note')
    if model == 'spesacommessa':
        rows = SpesaCommessa.objects.filter(id__in = re.findall("(\d+)",list)).values_list('data_registrazione', 'importo', 'protocollo__identificativo', 'protocollo__indirizzo', 'note')
    if model == 'spesagestione':
        rows = SpesaGestione.objects.filter(id__in = re.findall("(\d+)",list)).values_list('data_registrazione', 'importo', 'causale', 'fattura')
    if model == 'guadagnoeffettivo':
        rows = GuadagnoEffettivo.objects.filter(id__in = re.findall("(\d+)",list)).values_list('data_registrazione', 'importo')
    if model == 'consulenza':
        rows = Consulenza.objects.filter(id__in=re.findall("(\d+)", list)).values_list('data_registrazione', 'richiedente', 'indirizzo', 'attivita', 'compenso', 'note', 'data_scadenza', 'data_consegna', 'responsabile__cognome')
    if model == 'rubricaclienti':
        rows = RubricaClienti.objects.filter(tel__in=re.findall("(\d+)", list)).values_list('nominativo', 'tel', 'mail', 'note')
    if model == 'rubricareferenti':
        rows = RubricaReferenti.objects.filter(tel__in=re.findall("(\d+)", list)).values_list('nominativo', 'tel', 'mail', 'note')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, re.sub(r'<[^<]+?>', '', str(row[col_num]).replace("None", '')), font_style)
    wb.save(response)
    return response

def export_output_table_xls(request, numquery, year):
    output=''
    if int(numquery) == 1:
        output='spese_gestione'
        columns = ['Mese', 'Spese di gestione (€)', 'Daniele (€)', 'Laura (€)', 'Federico (€)']
        rows = execute_query_1(year)
    if int(numquery) == 2:
        output = 'ricavi'
        columns = ['Mese', 'Ricavi (€)', 'Daniele (€)', 'Laura (€)', 'Federico (€)']
        rows = execute_query_2(year)
    if int(numquery) == 3:
        output = 'guadagni_eff'
        columns = ['Mese', 'Guadagni Teorici (€)', 'Guadagni Effettivi (€)', 'Daniele (€)', 'Laura (€)', 'Federico (€)', 'GT - GE (€)']
        rows = execute_query_3(year)
    if int(numquery) == 4:
        output = 'contabilita_protocolli'
        columns = ['Identificativo', 'Cliente', 'Referente', 'Indirizzo', 'Pratica', 'Parcella', 'Entrate', 'Uscite', 'Saldo']
        rows = execute_query_4()
    wb = xlwt.Workbook(encoding='utf-8')
    if year == 'no':
        name_file = request.POST.get("fname")
        ws = wb.add_sheet(output)
    elif year:
        name_file = request.POST.get("fname") + '_' + year
        ws = wb.add_sheet(output+'_'+year)
    else:
        name_file = request.POST.get("fname")+'_YearNotSpecified'
        ws = wb.add_sheet(output + '_YearNotSpecified')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}.xls"'.format(name_file)
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]).replace("None",''), font_style)
    wb.save(response)
    return response
