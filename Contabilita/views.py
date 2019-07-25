from django.shortcuts import render,redirect
from django.contrib import messages
import re

from .forms import *
from django.db import connection
from .filters import *
from datetime import date,datetime
import xlwt
from django.http import HttpResponse


def viewhomepage(request):
    return render(request, "Homepage/HomePage.html")

def viewAllProtocols(request):
    protocolli = Protocollo.objects.all()
    sum_parcelle = 0
    protocollo_filter = ProtocolloFilter(request.GET, queryset=protocolli.order_by("-identificativo"))
    today = date.today()
    for proto in protocollo_filter.qs:
        d = datetime.strptime(str(proto.data_concordata), "%Y-%m-%d")
        data_concordata = d.date()
        if proto.data_effettiva != None:
            proto.status = None
        else:
            proto.status = (data_concordata - today).days
            cursor = connection.cursor()
            cursor.execute("""update Contabilita_protocollo set status = {} where identificativo = '{}'""".format(proto.status,proto.identificativo))
        sum_parcelle=sum_parcelle+proto.parcella

    context = {'filter': protocollo_filter, 'sum_p':sum_parcelle}
    return render(request, "Protocollo/AllProtocols.html", context)

def viewCreateProtocol(request):
    if(request.method == "POST"):
        form = formProtocol(request.POST)
        anno=form['data_registrazione'].value()[0:4]
        cursor = connection.cursor()
        cursor.execute("""select count from Contabilita_calendariocontatore as c where c.id={}""".format(anno))
        rows = cursor.fetchone()

        val=rows[0]+1
        cursor = connection.cursor()
        cursor.execute("""update Contabilita_calendariocontatore  set count={} where id={}""".format(str(val),anno))
        form.set_identificativo(str('{0:04}'.format(val))+"-"+anno[2:4])
        today = date.today()
        d = datetime.strptime(form['data_concordata'].value(), "%Y-%m-%d")
        data_concordata = d.date()
        if form['data_effettiva'].value() != '':
            form.set_status(0)
        else:
            form.set_status((data_concordata - today).days)

        if(form.is_valid()):
            form.save()
            return redirect('AllProtocols')
    else:
        form = formProtocol()
        return render(request,"Protocollo/CreateProtocol.html", {'form':form})

def viewDeleteProtocol(request,id):
    protocol = Protocollo.objects.get(id=id)
    protocol.delete()
    return redirect('AllProtocols')

def viewDeleteProtocolsGroup(request):
    if request.method == "POST":
        tasks = request.POST.getlist('list[]')
        for task in tasks:
            protocol = Protocollo.objects.get(id=int(task))
            protocol.delete()
        print("delete done")
    return render(request, "Homepage/HomePage.html")

def viewUpdateProtocol(request,id):
    if (request.method == "POST"):
        protocol = Protocollo.objects.get(id=id)
        form = formProtocolUpdate(request.POST, instance=protocol)
        if (form.is_valid()):
            form.save()
            return redirect('AllProtocols')
    else:
        protocol = Protocollo.objects.get(id=id)
        form = formProtocolUpdate(instance=protocol)
        return render(request, "Protocollo/UpdateProtocol.html", {'form': form})

def viewAllRicavi(request):
    ricavi = Ricavo.objects.all()
    ricavo_filter = RicavoFilter(request.GET, queryset=ricavi.order_by("-data"))
    sum_ricavi = 0
    for ricavo in ricavo_filter.qs:
        sum_ricavi = sum_ricavi + ricavo.importo
    context = {'filter': ricavo_filter, 'sum_r':sum_ricavi}
    return render(request, "Ricavo/AllRicavi.html", context)

def viewCreateRicavo(request):
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
            return redirect('AllRicavi')
    else:
        form = formRicavo()
        return render(request,"Ricavo/CreateRicavo.html",{'form':form})

def viewDeleteRicavo(request,id):
    ricavo = Ricavo.objects.get(id=id)
    ricavo.delete()
    return redirect('AllRicavi')

def viewDeleteRicaviGroup(request):
    if request.method == "POST":
        tasks = request.POST.getlist('list[]')
        for task in tasks:
            ricavo = Ricavo.objects.get(id=int(task))
            ricavo.delete()
        print("delete done")
    return render(request, "Homepage/HomePage.html")

def viewUpdateRicavo(request,id):
    if (request.method == "POST"):
        ricavo = Ricavo.objects.get(id=id)
        form = formRicavoUpdate(request.POST, instance=ricavo)
        if (form.is_valid()):
            if (form.Check1()):
                form.save()
            else:
                messages.error(request,
                               'ATTENZIONE. Il Ricavo inserito non rispetta i vincoli di parcella del protocollo')
            return redirect('AllRicavi')
        else:
            return redirect('AllRicavi')
    else:
        ricavo = Ricavo.objects.get(id=id)
        form = formRicavoUpdate(instance=ricavo)
        return render(request, "Ricavo/UpdateRicavo.html", {'form': form})

def viewAllSpeseCommessa(request):
    spesecommessa = SpesaCommessa.objects.all()
    spesacommessa_filter = SpesaCommessaFilter(request.GET, queryset=spesecommessa.order_by("-data"))
    sum_spesecommessa = 0
    for sc in spesacommessa_filter.qs:
        sum_spesecommessa = sum_spesecommessa + sc.importo
    return render(request, "SpesaCommessa/AllSpeseCommessa.html", {'filter': spesacommessa_filter, 'sum_s': sum_spesecommessa})

def viewCreateSpesaCommessa(request):
    if(request.method == "POST"):
        form = formSpesaCommessa(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('AllSpeseCommessa')
    else:
        form = formSpesaCommessa()
        return render(request,"SpesaCommessa/CreateSpesaCommessa.html",{'form':form})

def viewDeleteSpesaCommessa(request,id):
    spesacommessa = SpesaCommessa.objects.get(id=id)
    spesacommessa.delete()
    return redirect('AllSpeseCommessa')

def viewDeleteSpeseCommessaGroup(request):
    if request.method == "POST":
        tasks = request.POST.getlist('list[]')
        for task in tasks:
            spesacommessa = SpesaCommessa.objects.get(id=int(task))
            spesacommessa.delete()
        print("delete done")
    return render(request, "Homepage/HomePage.html")

def viewUpdateSpesaCommessa(request,id):
    if (request.method == "POST"):
        spesacommessa = SpesaCommessa.objects.get(id=id)
        form = formSpesaCommessaUpdate(request.POST, instance=spesacommessa)
        if (form.is_valid()):
            form.save()
            return redirect('AllSpeseCommessa')
    else:
        spesacommessa = SpesaCommessa.objects.get(id=id)
        form = formSpesaCommessaUpdate(instance=spesacommessa)
        return render(request, "SpesaCommessa/UpdateSpesaCommessa.html", {'form': form})

def viewAllSoci(request):
    soci = Socio.objects.all()
    return render(request, "Socio/AllSoci.html", { "tabella_soci" : soci })

def viewUpdateSocio(request,id):
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
                    messages.error(request,'ATTENZIONE. La percentuale inserita non รจ valida')
                    return redirect('AllSoci')
                else:
                    form.save()
                    return redirect('AllSoci')
    else:
        socio = Socio.objects.get(id=id)
        form = formSocio(instance=socio)
        return render(request, "Socio/UpdateSocio.html", {'form': form})

def viewAllSpeseGestione(request):
    spesegestione = SpesaGestione.objects.all()
    spesagestione_filter = SpesaGestioneFilter(request.GET, queryset=spesegestione.order_by("-data"))
    sum_spesegestione = 0
    for sg in spesagestione_filter.qs:
        sum_spesegestione = sum_spesegestione + sg.importo
    return render(request, "SpesaGestione/AllSpeseGestione.html", {'filter': spesagestione_filter, 'sum_s':sum_spesegestione})

def viewCreateSpesaGestione(request):
    if(request.method == "POST"):
        form = formSpesaGestione(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('AllSpeseGestione')
    else:
        form = formSpesaGestione()
        return render(request,"SpesaGestione/CreateSpesaGestione.html",{'form':form})

def viewDeleteSpesaGestione(request,id):
    spesagestione = SpesaGestione.objects.get(id=id)
    spesagestione.delete()
    return redirect('AllSpeseGestione')

def viewDeleteSpeseGestioneGroup(request):
    if request.method == "POST":
        tasks = request.POST.getlist('list[]')
        for task in tasks:
            spesagestione = SpesaGestione.objects.get(id=int(task))
            spesagestione.delete()
        print("delete done")
    return render(request, "Homepage/HomePage.html")

def viewUpdateSpesaGestione(request,id):
    if (request.method == "POST"):
        spesagestione = SpesaGestione.objects.get(id=id)
        form = formSpesaGestioneUpdate(request.POST, instance=spesagestione)
        if (form.is_valid()):
            form.save()
            return redirect('AllSpeseGestione')
    else:
        spesagestione = SpesaGestione.objects.get(id=id)
        form = formSpesaGestioneUpdate(instance=spesagestione)
        return render(request, "SpesaGestione/UpdateSpesaGestione.html", {'form': form})

def viewAllGuadagniEffettivi(request):
    guadagnieffettivi = GuadagnoEffettivo.objects.all()
    guadagnoeffettivo_filter = GuadagnoEffettivoFilter(request.GET, queryset=guadagnieffettivi.order_by("-data"))
    sum_guadagnieffettivi = 0
    for ge in guadagnoeffettivo_filter.qs:
        sum_guadagnieffettivi = sum_guadagnieffettivi + ge.importo
    return render(request, "GuadagnoEffettivo/AllGuadagniEffettivi.html", { "filter" : guadagnoeffettivo_filter, 'sum_g': sum_guadagnieffettivi})

def viewCreateGuadagnoEffettivo(request):
    if(request.method == "POST"):
        form = formGuadagnoEffettivo(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('AllGuadagniEffettivi')
    else:
        form = formGuadagnoEffettivo()
        return render(request,"GuadagnoEffettivo/CreateGuadagnoEffettivo.html",{'form':form})

def viewDeleteGuadagnoEffettivo(request,id):
    guadagnoefettivo = GuadagnoEffettivo.objects.get(id=id)
    guadagnoefettivo.delete()
    return redirect('AllGuadagniEffettivi')

def viewDeleteGuadagniEffettiviGroup(request):
    if request.method == "POST":
        tasks = request.POST.getlist('list[]')
        for task in tasks:
            guadagnoeffettivo = GuadagnoEffettivo.objects.get(id=int(task))
            guadagnoeffettivo.delete()
        print("delete done")
    return render(request, "Homepage/HomePage.html")

def viewUpdateGuadagnoEffettivo(request,id):
    if (request.method == "POST"):
        guadagnoeffettivo = GuadagnoEffettivo.objects.get(id=id)
        form = formGuadagnoEffettivoUpdate(request.POST, instance=guadagnoeffettivo)
        if (form.is_valid()):
            form.save()
            return redirect('AllGuadagniEffettivi')
    else:
        ricavoeffettivo = GuadagnoEffettivo.objects.get(id=id)
        form = formGuadagnoEffettivoUpdate(instance=ricavoeffettivo)
        return render(request, "GuadagnoEffettivo/UpdateGuadagnoEffettivo.html", {'form': form})

def execute_query_1(year):
    anno = str(year)
    query = """select '01/GENNAIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data >= '{d[year]}-01-01' and t1.data <= '{d[year]}-01-31' 
                        UNION
                        select '02/FEBBRAIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data >= '{d[year]}-02-01' and t1.data <= '{d[year]}-02-28' 
                        UNION
                        select '03/MARZO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data >= '{d[year]}-03-01' and t1.data <= '{d[year]}-03-31'
                        UNION
                        select '04/APRILE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data >= '{d[year]}-04-01' and t1.data <= '{d[year]}-04-30' 
                        UNION
                        select '05/MAGGIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data >= '{d[year]}-05-01' and t1.data <= '{d[year]}-05-31' 
                        UNION
                        select '06/GIUGNO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data >= '{d[year]}-06-01' and t1.data <= '{d[year]}-06-30' 
                        UNION
                        select '07/LUGLIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data >= '{d[year]}-07-01' and t1.data <= '{d[year]}-07-31' 
                        UNION
                        select '08/AGOSTO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data >= '{d[year]}-08-01' and t1.data <= '{d[year]}-08-31' 
                        UNION
                        select '09/SETTEMBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data >= '{d[year]}-09-01' and t1.data <= '{d[year]}-09-30' 
                        UNION
                        select '10/OTTOBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data >= '{d[year]}-10-01' and t1.data <= '{d[year]}-10-31' 
                        UNION
                        select '11/NOVEMBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data >= '{d[year]}-11-01' and t1.data <= '{d[year]}-11-30' 
                        UNION
                        select '12/DICEMBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1  
                        where t1.data >= '{d[year]}-12-01' and t1.data <= '{d[year]}-12-31'
                        UNION
                        select 'TOTALE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_spesagestione t1
                        where t1.data >= '{d[year]}-01-01' and t1.data <= '{d[year]}-12-31'
                        ORDER BY mese ASC;""".format(d={'year': anno})

    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def viewResocontoSpeseGestione(request):
    if (request.method == "POST"):
        form = form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(request.POST)
        if (form.is_valid()):
            return render(request, "ResocontoSpeseGestione.html", {'form': form, 'tabella_output1': execute_query_1(form['year'].value()), 'year': form['year'].value()})
    else:
        form = form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi()
        return render(request, "ResocontoSpeseGestione.html", {'form': form, 'tabella_output1':[]})

def execute_query_2(year):
    anno = str(year)

    query = """select '01/GENNAIO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico
                        from Contabilita_ricavo t1  
                        where t1.data >= '{d[year]}-01-01' and t1.data <= '{d[year]}-01-31' 

                        union

                        select '02/FEBBRAIO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_ricavo t1  
                        where t1.data >= '{d[year]}-02-01' and t1.data <= '{d[year]}-02-28' 

                        union

                        select '03/MARZO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_ricavo t1  
                        where t1.data >= '{d[year]}-03-01' and t1.data <= '{d[year]}-03-31' 

                        union

                        select '04/APRILE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_ricavo t1
                        where t1.data >= '{d[year]}-04-01' and t1.data <= '{d[year]}-04-30' 

                        union

                        select '05/MAGGIO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_ricavo t1
                        where t1.data >= '{d[year]}-05-01' and t1.data <= '{d[year]}-05-31' 

                        union

                        select '06/GIUGNO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_ricavo t1
                        where t1.data >= '{d[year]}-06-01' and t1.data <= '{d[year]}-06-30' 

                        union

                        select '07/LUGLIO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_ricavo t1
                        where t1.data >= '{d[year]}-07-01' and t1.data <= '{d[year]}-07-31' 

                        union

                        select '08/AGOSTO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_ricavo t1
                        where t1.data >= '{d[year]}-08-01' and t1.data <= '{d[year]}-08-31' 

                        union

                        select '09/SETTEMBRE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_ricavo t1
                        where t1.data >= '{d[year]}-09-01' and t1.data <= '{d[year]}-09-30' 

                        union

                        select '10/OTTOBRE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_ricavo t1
                        where t1.data >= '{d[year]}-10-01' and t1.data <= '{d[year]}-10-31' 

                        union

                        select '11/NOVEMBRE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_ricavo t1
                        where t1.data >= '{d[year]}-11-01' and t1.data <= '{d[year]}-11-30' 

                        union

                        select '12/DICEMBRE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_ricavo t1
                        where t1.data >= '{d[year]}-12-01' and t1.data <= '{d[year]}-12-31' 

                        union

                        select 'TOTALE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                        from Contabilita_ricavo t1
                        where t1.data >= '{d[year]}-01-01' and t1.data <= '{d[year]}-12-31'

                        ORDER BY mese ASC;""".format(d={'year': anno})

    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def viewResocontoRicavi(request):
    if (request.method == "POST"):
        form = form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(request.POST)
        if (form.is_valid()):
            return render(request, "ResocontoRicavi.html", {'form': form, 'tabella_output2': execute_query_2(form['year'].value()), 'year': form['year'].value()})
    else:
        form = form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi()
        return render(request, "ResocontoRicavi.html", {'form': form, 'tabella_output2':[]})

def execute_query_3(year):
    anno = str(year)
    query = """select '01/GENNAIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-01-01' and t2.data <= '{d[year]}-01-31') -
              (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-01-01' and t1.data <= '{d[year]}-01-31') as GuadagniTeorici,
              coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
              (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-01-01' and t2.data <= '{d[year]}-01-31') -
              (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-01-01' and t1.data <= '{d[year]}-01-31')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1

            Where t1.data >= '{d[year]}-01-01' and t1.data <= '{d[year]}-01-31'

            union

            select '02/FEBBRAIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-02-01' and t2.data <= '{d[year]}-02-28') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-02-01' and t1.data <= '{d[year]}-02-28') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-02-01' and t2.data <= '{d[year]}-02-28') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-02-01' and t1.data <= '{d[year]}-02-28')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1

            Where t1.data >= '{d[year]}-02-01' and t1.data <= '{d[year]}-02-28'

            union

            select '03/MARZO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-03-01' and t2.data <= '{d[year]}-03-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-03-01' and t1.data <= '{d[year]}-03-31') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-03-01' and t2.data <= '{d[year]}-03-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-03-01' and t1.data <= '{d[year]}-03-31')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1

            Where t1.data >= '{d[year]}-03-01' and t1.data <= '{d[year]}-03-31'

            union

            select '04/APRILE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-04-01' and t2.data <= '{d[year]}-04-30') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-04-01' and t1.data <= '{d[year]}-04-30') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-04-01' and t2.data <= '{d[year]}-04-30') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-04-01' and t1.data <= '{d[year]}-04-30')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1

            Where t1.data >= '{d[year]}-04-01' and t1.data <= '{d[year]}-04-30'

            union

            select '05/MAGGIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-05-01' and t2.data <= '{d[year]}-05-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-05-01' and t1.data <= '{d[year]}-05-31') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-05-01' and t2.data <= '{d[year]}-05-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-05-01' and t1.data <= '{d[year]}-05-31')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1

            Where t1.data >= '{d[year]}-05-01' and t1.data <= '{d[year]}-05-31'

            union

            select '06/GIUGNO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-06-01' and t2.data <= '{d[year]}-06-30') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-06-01' and t1.data <= '{d[year]}-06-30') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-06-01' and t2.data <= '{d[year]}-06-30') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-06-01' and t1.data <= '{d[year]}-06-30')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1

            Where t1.data >= '{d[year]}-06-01' and t1.data <= '{d[year]}-06-30'

            union

            select '07/LUGLIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-07-01' and t2.data <= '{d[year]}-07-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-07-01' and t1.data <= '{d[year]}-07-31') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-07-01' and t2.data <= '{d[year]}-07-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-07-01' and t1.data <= '{d[year]}-07-31')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1

            Where t1.data >= '{d[year]}-07-01' and t1.data <= '{d[year]}-07-31'

            union

            select '08/AGOSTO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-08-01' and t2.data <= '{d[year]}-08-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-08-01' and t1.data <= '{d[year]}-08-31') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-08-01' and t2.data <= '{d[year]}-08-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-08-01' and t1.data <= '{d[year]}-08-31')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1

            Where t1.data >= '{d[year]}-08-01' and t1.data <= '{d[year]}-08-31'

            union

            select '09/SETTEMBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-09-01' and t2.data <= '{d[year]}-09-30') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-09-01' and t1.data <= '{d[year]}-09-30') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-09-01' and t2.data <= '{d[year]}-09-30') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-09-01' and t1.data <= '{d[year]}-09-30')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1

            Where t1.data >= '{d[year]}-09-01' and t1.data <= '{d[year]}-09-30'

            union

            select '10/OTTOBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-10-01' and t2.data <= '{d[year]}-10-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-10-01' and t1.data <= '{d[year]}-10-31') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-10-01' and t2.data <= '{d[year]}-10-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-10-01' and t1.data <= '{d[year]}-10-31')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1

            Where t1.data >= '{d[year]}-10-01' and t1.data <= '{d[year]}-10-31'

            union

            select '11/NOVEMBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-11-01' and t2.data <= '{d[year]}-11-30') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-11-01' and t1.data <= '{d[year]}-11-30') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-11-01' and t2.data <= '{d[year]}-11-30') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-11-01' and t1.data <= '{d[year]}-11-30')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1

            Where t1.data >= '{d[year]}-11-01' and t1.data <= '{d[year]}-11-30'

            union

            select '12/DICEMBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-12-01' and t2.data <= '{d[year]}-12-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-12-01' and t1.data <= '{d[year]}-12-31') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '{d[year]}-12-01' and t2.data <= '{d[year]}-12-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '{d[year]}-12-01' and t1.data <= '{d[year]}-12-31')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1

            Where t1.data >= '2018-12-01' and t1.data <= '2018-12-31'

            union

            select 'TOTALE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 Where t2.data >= '{d[year]}-01-01' and t2.data <= '{d[year]}-12-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 Where t1.data >= '{d[year]}-01-01' and t1.data <= '{d[year]}-12-31') as GuadagniTeorici,
                                      coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                      (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 Where t2.data >= '{d[year]}-01-01' and t2.data <= '{d[year]}-12-31') -
                                      (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 Where t1.data >= '{d[year]}-01-01' and t1.data <= '{d[year]}-12-31')-coalesce(sum(t1.importo),0) as DIfferenza
            from Contabilita_guadagnoeffettivo t1

            Where t1.data >= '{d[year]}-01-01' and t1.data <= '{d[year]}-12-31'	  

            ORDER BY mese ASC;""".format(d={'year': anno})

    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def viewGestioneGuadagniEffettivi(request):
    if (request.method == "POST"):
        form = form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(request.POST)
        if (form.is_valid()):
            return render(request, "GestioneGuadagniEffettivi.html", {'form': form, 'tabella_output3': execute_query_3(form['year'].value()), 'year': form['year'].value()})
    else:
        form = form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi()
        return render(request, "GestioneGuadagniEffettivi.html", {'form': form, 'tabella_output3': []})

def execute_query_4():
    query = """SELECT t1.identificativo, t1.cliente, t1.referente, t1.indirizzo,t1.pratica,t1.parcella,(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id) as entrate,
                                        (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as uscite,
                                        t1.parcella-(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id)+
                                        (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as saldo
            FROM   Contabilita_protocollo t1
            WHERE saldo != 0

            union

            SELECT t1.identificativo, t1.cliente, t1.referente, t1.indirizzo,t1.pratica,t1.parcella,(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id) as entrate,
                                        (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as uscite,
                                        t1.parcella-(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id)+
                                        (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as saldo
            FROM   Contabilita_protocollo t1
            WHERE saldo != 0"""
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    print(type(rows))
    print(rows)
    return rows

def viewContabilitaProtocolli(request):
    return render(request, "ContabilitaProtocolli.html", {'tabella_output4': execute_query_4()})

def export_input_table_xlsx(request,list,model):
    fields_models = { 'protocollo': ['Identificativo', 'Cliente', 'Referente', 'Mail Cliente', 'Tel Cliente', 'Indirizzo', 'Parcella', 'Pratica', 'Note', 'Data Registrazione', 'Data Concordata', 'Data Effettiva'],
                      'ricavo' : ['Data','Movimento','Importo','Fattura','Intestatario Fattura','Protocollo'],
                      'spesacommessa' : ['Data','Importo','Protocollo'],
                      'spesagestione' : ['Data', 'Importo', 'Fattura', 'Intestatario Fattura', 'Causale'],
                      'guadagnoeffettivo' : ['Data', 'Importo']}
    name_file = request.POST.get("fname") or 'default_name_{}'.format(model)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}.xlsx"'.format(name_file)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(name_file)
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
        rows = Protocollo.objects.filter(identificativo__in = re.findall("(\d+-\d+)",list)).values_list('identificativo', 'cliente', 'referente', 'mail_cliente', 'tel_cliente', 'indirizzo', 'parcella', 'pratica', 'note', 'data_registrazione','data_concordata' , 'data_effettiva')
    if model == 'ricavo':
        rows = Ricavo.objects.filter(id__in = re.findall("(\d+)",list)).values_list('data', 'movimento', 'importo', 'fattura', 'intestatario_fattura', 'protocollo')
    if model == 'spesacommessa':
        rows = SpesaCommessa.objects.filter(id__in = re.findall("(\d+)",list)).values_list('data', 'importo', 'protocollo')
    if model == 'spesagestione':
        rows = SpesaGestione.objects.filter(id__in = re.findall("(\d+)",list)).values_list('data', 'importo', 'fattura', 'intestatario_fattura', 'causale')
    if model == 'guadagnoeffettivo':
        rows = GuadagnoEffettivo.objects.filter(id__in = re.findall("(\d+)",list)).values_list('data', 'importo')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response

def export_output_table_xlsx(request, numquery, year):
    output=''
    if int(numquery) == 1:
        output='spese_gestione'
        columns = ['Mese', 'Spese di gestione (€)', 'Daniele (€)', 'Laura (€)', 'Federico (€)']
        rows = execute_query_1(year)
    if int(numquery) == 2:
        output = 'resoconto_ricavi'
        columns = ['Mese', 'Ricavi (€)', 'Daniele (€)', 'Laura (€)', 'Federico (€)']
        rows = execute_query_2(year)
    if int(numquery) == 3:
        output = 'gestione_guadagni_effettivi'
        columns = ['Mese', 'Guadagni Teorici (€)', 'Guadagni Effettivi (€)', 'Daniele (€)', 'Laura (€)', 'Federico (€)', 'GT - GE (€)']
        rows = execute_query_3(year)
    if int(numquery) == 4:
        output = 'contabilita_protocolli'
        columns = ['Identificativo', 'Cliente', 'Referente', 'Indirizzo', 'Pratica', 'Parcella', 'Entrate', 'Uscite', 'Saldo']
        rows = execute_query_4()

    name_file = request.POST.get("fname")+'_'+year or 'default_name_{}_{}'.format(output, year or 'YearNotSpecified')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}.xlsx"'.format(name_file)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(output)
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response



