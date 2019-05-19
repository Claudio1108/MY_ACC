from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import *
from django.db import connection
from .filters import *
from django.core.paginator import Paginator

# Create your views here.

def viewhomepage(request):

    return render(request, "Homepage/HomePage.html")

def viewAllProtocols(request):

    protocolli = Protocollo.objects.all()

    protocollo_filter = ProtocolloFilter(request.GET, queryset=protocolli.order_by("-identificativo","-parcella"))

    sum_parcelle=0

    for i in range(0,len(protocollo_filter.qs),1):

        sum_parcelle=sum_parcelle+protocollo_filter.qs[i].parcella

    context = {'filter': protocollo_filter, 'sum_p':sum_parcelle}

    return render(request, "Protocollo/AllProtocols.html", context)

def viewCreateProtocol(request):

    if(request.method == "POST"):

        #creiamo l'istanza del form e la popoliamo con i dati della POST request ("processo di binding")

        form = formProtocol(request.POST)
        anno=form['data'].value()[0:4]
        query1 = """select count from Contabilita_calendariocontatore as c where c.id="""+anno
        print(query1)
        cursor = connection.cursor()
        cursor.execute(query1)
        rows = cursor.fetchone()

        print(type(rows[0]))
        print(rows[0])
        val=rows[0]+1

        query2="""update Contabilita_calendariocontatore  set count="""+str(val)+""" where id="""+anno
        print(query2)
        cursor = connection.cursor()
        cursor.execute(query2)
        form.set_identificativo(str(val)+"-"+anno[2:4])

        if(form.is_valid()):

            print("il form è valido")
            print(str(form['identificativo'].value()))
            new_protocol = form.save()
            print("new_protocol: ",new_protocol)
            return redirect ('AllProtocols')

    else:

        form = formProtocol()
        context={'form':form}
        return render(request,"Protocollo/CreateProtocol.html",context)


def viewDeleteProtocol(request,id):

    protocol = Protocollo.objects.get(id=id)
    protocol.delete()
    return redirect('AllProtocols')

def viewDeleteProtocolsGroup(request):
    if request.method == "POST":
        tasks = request.POST.getlist('list[]')
        print(str(tasks))
        for i in range(0,len(tasks),1):
            protocol = Protocollo.objects.get(id=int(tasks[i]))
            protocol.delete()

        print("delete done")

    return render(request, "Homepage/HomePage.html")

def viewUpdateProtocol(request,id):
    if (request.method == "POST"):

        # creiamo l'istanza del form e la popoliamo con i dati della POST request ("processo di binding")
        protocol = Protocollo.objects.get(id=id)
        form = formProtocolUpdate(request.POST, instance=protocol)

        if (form.is_valid()):
            print("il form è valido")
            new_protocol = form.save()
            print("new_protocol: ", new_protocol)
            return redirect('AllProtocols')

    else:
        protocol = Protocollo.objects.get(id=id)
        form = formProtocolUpdate(instance=protocol)
        context = {'form': form}
        return render(request, "Protocollo/UpdateProtocol.html", context)


def viewAllRicavi(request):

    ricavi = Ricavo.objects.all()

    ricavo_filter = RicavoFilter(request.GET, queryset=ricavi)

    sum_ricavi = 0

    for i in range(0, len(ricavo_filter.qs), 1):
        sum_ricavi = sum_ricavi + ricavo_filter.qs[i].importo

    context = {'filter': ricavo_filter, 'sum_r':sum_ricavi}

    return render(request, "Ricavo/AllRicavi.html", context)


def viewCreateRicavo(request):

    if(request.method == "POST"):

        #creiamo l'istanza del form e la popoliamo con i dati della POST request ("processo di binding")

        form = formRicavo(request.POST)
        if(form.is_valid()):
            print("il form è valido")
            if(form['protocollo'].value()!=""):
                if(form.Check1()==True):
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

        context={'form':form}

        return render(request,"Ricavo/CreateRicavo.html",context)


def viewDeleteRicavo(request,id):

    ricavo = Ricavo.objects.get(id=id)
    ricavo.delete()
    return redirect('AllRicavi')

def viewDeleteRicaviGroup(request):
    if request.method == "POST":
        tasks = request.POST.getlist('list[]')
        print(str(tasks))
        for i in range(0,len(tasks),1):
            ricavo = Ricavo.objects.get(id=int(tasks[i]))
            ricavo.delete()

        print("delete done")

    return render(request, "Homepage/HomePage.html")

def viewUpdateRicavo(request,id):
    if (request.method == "POST"):

        # creiamo l'istanza del form e la popoliamo con i dati della POST request ("processo di binding")
        ricavo = Ricavo.objects.get(id=id)
        form = formRicavoUpdate(request.POST, instance=ricavo)

        if (form.is_valid()):
            print("il form è valido")
            if (form.Check1() == True):
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
        context = {'form': form}
        return render(request, "Ricavo/UpdateRicavo.html", context)


def viewAllSpeseCommessa(request):

    spesecommessa = SpesaCommessa.objects.all()

    sum_spesecommessa = 0

    for i in range(0, len(spesecommessa), 1):
        sum_spesecommessa = sum_spesecommessa + spesecommessa[i].importo

    context = { "tabella_spesecommessa" : spesecommessa, 'sum_s': sum_spesecommessa}

    return render(request, "SpesaCommessa/AllSpeseCommessa.html", context)


def viewCreateSpesaCommessa(request):

    if(request.method == "POST"):

        #creiamo l'istanza del form e la popoliamo con i dati della POST request ("processo di binding")

        form = formSpesaCommessa(request.POST)
        if(form.is_valid()):
            print("il form è valido")
            form.save()
            return redirect('AllSpeseCommessa')

    else:

        form = formSpesaCommessa()

        context={'form':form}

        return render(request,"SpesaCommessa/CreateSpesaCommessa.html",context)

def viewDeleteSpesaCommessa(request,id):

    spesacommessa = SpesaCommessa.objects.get(id=id)
    spesacommessa.delete()
    return redirect('AllSpeseCommessa')

def viewDeleteSpeseCommessaGroup(request):
    if request.method == "POST":
        tasks = request.POST.getlist('list[]')
        print(str(tasks))
        for i in range(0,len(tasks),1):
            spesacommessa = SpesaCommessa.objects.get(id=int(tasks[i]))
            spesacommessa.delete()

        print("delete done")

    return render(request, "Homepage/HomePage.html")

def viewUpdateSpesaCommessa(request,id):
    if (request.method == "POST"):

        # creiamo l'istanza del form e la popoliamo con i dati della POST request ("processo di binding")
        spesacommessa = SpesaCommessa.objects.get(id=id)
        form = formSpesaCommessaUpdate(request.POST, instance=spesacommessa)

        if (form.is_valid()):
            print("il form è valido")
            form.save()
            return redirect('AllSpeseCommessa')

    else:
        spesacommessa = SpesaCommessa.objects.get(id=id)
        form = formSpesaCommessaUpdate(instance=spesacommessa)
        context = {'form': form}
        return render(request, "SpesaCommessa/UpdateSpesaCommessa.html", context)

def viewAllSoci(request):

    soci = Socio.objects.all()

    context = { "tabella_soci" : soci }

    return render(request, "Socio/AllSoci.html", context)

def viewUpdateSocio(request,id):
    if (request.method == "POST"):

        # creiamo l'istanza del form e la popoliamo con i dati della POST request ("processo di binding")
        socio = Socio.objects.get(id=id)
        form = formSocio(request.POST, instance=socio)
        soci = Socio.objects.all()
        sum=0
        for i in range(0,len(soci),1):

            if(soci[i].id != id):

                sum+=soci[i].percentuale

        if (form.is_valid()):
            print("il form è valido")

            if(float(sum)+float(form['percentuale'].value()) < 1.00):

                form.save()
                messages.warning(request,'Le percentuali non sono distrubuite completamente')
                return redirect('AllSoci')

            else:

                if (float(sum) + float(form['percentuale'].value()) > 1.00):
                    messages.error(request,'ATTENZIONE. La percentuale inserita non è valida')
                    return redirect('AllSoci')
                else:
                    form.save()
                    return redirect('AllSoci')

    else:
        socio = Socio.objects.get(id=id)
        form = formSocio(instance=socio)
        context = {'form': form}
        return render(request, "Socio/UpdateSocio.html", context)

def viewAllSpeseGestione(request):

    spesegestione = SpesaGestione.objects.all()

    spesagestione_filter = SpesaGestioneFilter(request.GET, queryset=spesegestione)

    sum_spesegestione = 0

    for i in range(0, len(spesagestione_filter.qs), 1):
        sum_spesegestione = sum_spesegestione + spesagestione_filter.qs[i].importo

    context = {'filter': spesagestione_filter, 'sum_s':sum_spesegestione}

    return render(request, "SpesaGestione/AllSpeseGestione.html", context)


def viewCreateSpesaGestione(request):

    if(request.method == "POST"):

        #creiamo l'istanza del form e la popoliamo con i dati della POST request ("processo di binding")

        form = formSpesaGestione(request.POST)
        if(form.is_valid()):
            print("il form è valido")
            form.save()
            return redirect('AllSpeseGestione')

    else:

        form = formSpesaGestione()

        context={'form':form}

        return render(request,"SpesaGestione/CreateSpesaGestione.html",context)

def viewDeleteSpesaGestione(request,id):

    spesagestione = SpesaGestione.objects.get(id=id)
    spesagestione.delete()
    return redirect('AllSpeseGestione')

def viewDeleteSpeseGestioneGroup(request):
    if request.method == "POST":
        tasks = request.POST.getlist('list[]')
        print(str(tasks))
        for i in range(0,len(tasks),1):
            spesagestione = SpesaGestione.objects.get(id=int(tasks[i]))
            spesagestione.delete()

        print("delete done")

    return render(request, "Homepage/HomePage.html")

def viewUpdateSpesaGestione(request,id):
    if (request.method == "POST"):

        # creiamo l'istanza del form e la popoliamo con i dati della POST request ("processo di binding")
        spesagestione = SpesaGestione.objects.get(id=id)
        form = formSpesaGestioneUpdate(request.POST, instance=spesagestione)

        if (form.is_valid()):
            print("il form è valido")
            form.save()
            return redirect('AllSpeseGestione')
    else:
        spesagestione = SpesaGestione.objects.get(id=id)
        form = formSpesaGestioneUpdate(instance=spesagestione)
        context = {'form': form}
        return render(request, "SpesaGestione/UpdateSpesaGestione.html", context)

def viewAllGuadagniEffettivi(request):

    guadagnieffettivi = GuadagnoEffettivo.objects.all()

    sum_guadagnieffettivi = 0

    for i in range(0, len(guadagnieffettivi), 1):
        print(str(guadagnieffettivi[i].importo))
        sum_guadagnieffettivi = sum_guadagnieffettivi + guadagnieffettivi[i].importo
    print(str(sum_guadagnieffettivi))
    context = { "tabella_guadagniffettivi" : guadagnieffettivi, 'sum_g': sum_guadagnieffettivi}

    return render(request, "GuadagnoEffettivo/AllGuadagniEffettivi.html", context)


def viewCreateGuadagnoEffettivo(request):

    if(request.method == "POST"):

        #creiamo l'istanza del form e la popoliamo con i dati della POST request ("processo di binding")

        form = formGuadagnoEffettivo(request.POST)
        if(form.is_valid()):
            print("il form è valido")
            form.save()
            return redirect('AllGuadagniEffettivi')

    else:

        form = formGuadagnoEffettivo()

        context={'form':form}

        return render(request,"GuadagnoEffettivo/CreateGuadagnoEffettivo.html",context)

def viewDeleteGuadagnoEffettivo(request,id):

    guadagnoefettivo = GuadagnoEffettivo.objects.get(id=id)
    guadagnoefettivo.delete()
    return redirect('AllGuadagniEffettivi')

def viewDeleteGuadagniEffettiviGroup(request):
    if request.method == "POST":
        tasks = request.POST.getlist('list[]')
        print(str(tasks))
        for i in range(0,len(tasks),1):
            guadagnoeffettivo = GuadagnoEffettivo.objects.get(id=int(tasks[i]))
            guadagnoeffettivo.delete()

        print("delete done")

    return render(request, "Homepage/HomePage.html")

def viewUpdateGuadagnoEffettivo(request,id):

    if (request.method == "POST"):

        # creiamo l'istanza del form e la popoliamo con i dati della POST request ("processo di binding")
        guadagnoeffettivo = GuadagnoEffettivo.objects.get(id=id)
        form = formGuadagnoEffettivoUpdate(request.POST, instance=guadagnoeffettivo)

        if (form.is_valid()):
            print("il form è valido")
            form.save()
            return redirect('AllGuadagniEffettivi')

    else:
        ricavoeffettivo = GuadagnoEffettivo.objects.get(id=id)
        form = formGuadagnoEffettivoUpdate(instance=ricavoeffettivo)
        context = {'form': form}
        return render(request, "GuadagnoEffettivo/UpdateGuadagnoEffettivo.html", context)


def viewResocontoSpeseGestione(request):

    if (request.method == "POST"):

        form = formResocontoSpeseGestione(request.POST)

        if (form.is_valid()):
            anno=str(form['year'].value())
            print(anno)
            print(type(anno))

            query="""select '01/GENNAIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-01-31' 
                    UNION
                    select '02/FEBBRAIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-02-01' and t1.data <= '"""+anno+"""-02-28' 
                    UNION
                    select '03/MARZO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-03-01' and t1.data <= '"""+anno+"""-03-31'
                    UNION
                    select '04/APRILE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-04-01' and t1.data <= '"""+anno+"""-04-30' 
                    UNION
                    select '05/MAGGIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-05-01' and t1.data <= '"""+anno+"""-05-31' 
                    UNION
                    select '06/GIUGNO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-06-01' and t1.data <= '"""+anno+"""-06-30' 
                    UNION
                    select '07/LUGLIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-07-01' and t1.data <= '"""+anno+"""-07-31' 
                    UNION
                    select '08/AGOSTO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-08-01' and t1.data <= '"""+anno+"""-08-31' 
                    UNION
                    select '09/SETTEMBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-09-01' and t1.data <= '"""+anno+"""-09-30' 
                    UNION
                    select '10/OTTOBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-10-01' and t1.data <= '"""+anno+"""-10-31' 
                    UNION
                    select '11/NOVEMBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-11-01' and t1.data <= '"""+anno+"""-11-30' 
                    UNION
                    select '12/DICEMBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-12-01' and t1.data <= '"""+anno+"""-12-31'
                    UNION
                    select 'TOTALE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_spesagestione t1
                    where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-12-31'
                    ORDER BY mese ASC;"""

            print(query)
            cursor = connection.cursor()
            cursor.execute(query);
            rows = cursor.fetchall()
            print(rows)

            context = {'form': form, 'tabella_output1':rows}
            return render(request, "ResocontoSpeseGestione.html", context)

    else:

        rows=[]
        form = formResocontoSpeseGestione()
        context = {'form': form, 'tabella_output1':rows}
        return render(request, "ResocontoSpeseGestione.html", context)


def viewResocontoRicavi(request):

    if (request.method == "POST"):

        form = formResocontoRicavi(request.POST)

        if (form.is_valid()):
            anno=str(form['year'].value())
            print(anno)
            print(type(anno))

            query="""select '01/GENNAIO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico
                    from Contabilita_ricavo t1  
                    where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-01-31' 
                    
                    union
                    
                    select '02/FEBBRAIO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1  
                    where t1.data >= '"""+anno+"""-02-01' and t1.data <= '"""+anno+"""-02-28' 
                    
                    union
                    
                    select '03/MARZO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1  
                    where t1.data >= '"""+anno+"""-03-01' and t1.data <= '"""+anno+"""-03-31' 
                    
                    union
                    
                    select '04/APRILE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where t1.data >= '"""+anno+"""-04-01' and t1.data <= '"""+anno+"""-04-30' 
                    
                    union
                    
                    select '05/MAGGIO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where t1.data >= '"""+anno+"""-05-01' and t1.data <= '"""+anno+"""-05-31' 
                    
                    union
                    
                    select '06/GIUGNO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where t1.data >= '"""+anno+"""-06-01' and t1.data <= '"""+anno+"""-06-30' 
                    
                    union
                    
                    select '07/LUGLIO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where t1.data >= '"""+anno+"""-07-01' and t1.data <= '"""+anno+"""-07-31' 
                    
                    union
                    
                    select '08/AGOSTO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where t1.data >= '"""+anno+"""-08-01' and t1.data <= '"""+anno+"""-08-31' 
                    
                    union
                    
                    select '09/SETTEMBRE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where t1.data >= '"""+anno+"""-09-01' and t1.data <= '"""+anno+"""-09-30' 
                    
                    union
                    
                    select '10/OTTOBRE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where t1.data >= '"""+anno+"""-10-01' and t1.data <= '"""+anno+"""-10-31' 
                    
                    union
                    
                    select '11/NOVEMBRE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where t1.data >= '"""+anno+"""-11-01' and t1.data <= '"""+anno+"""-11-30' 
                    
                    union
                    
                    select '12/DICEMBRE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where t1.data >= '"""+anno+"""-12-01' and t1.data <= '"""+anno+"""-12-31' 
                    
                    union
                    
                    select 'TOTALE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-12-31'
                    
                    ORDER BY mese ASC;"""

            print(query)
            cursor = connection.cursor()
            cursor.execute(query);
            rows = cursor.fetchall()
            print(rows)

            context = {'form': form, 'tabella_output2':rows}
            return render(request, "ResocontoRicavi.html", context)




    else:

        rows=[]
        form = formResocontoRicavi()
        context = {'form': form, 'tabella_output2':rows}
        return render(request, "ResocontoRicavi.html", context)

def viewGestioneGuadagniEffettivi(request):
    if (request.method == "POST"):

        form = formGestioneGuadagniEffettivi(request.POST)

        if (form.is_valid()):
            anno = str(form['year'].value())
            print(anno)
            print(type(anno))

            query = """select '01/GENNAIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-01-01' and t2.data <= '"""+anno+"""-01-31') -
						  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-01-31') as GuadagniTeorici,
						  coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
						  (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-01-01' and t2.data <= '"""+anno+"""-01-31') -
						  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-01-31')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_guadagnoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-01-31'
                        
                        union
                        
                        select '02/FEBBRAIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-02-01' and t2.data <= '"""+anno+"""-02-28') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-02-01' and t1.data <= '"""+anno+"""-02-28') as GuadagniTeorici,
                                                  coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-02-01' and t2.data <= '"""+anno+"""-02-28') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-02-01' and t1.data <= '"""+anno+"""-02-28')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_guadagnoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-02-01' and t1.data <= '"""+anno+"""-02-28'
                        
                        union
                        
                        select '03/MARZO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-03-01' and t2.data <= '"""+anno+"""-03-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-03-01' and t1.data <= '"""+anno+"""-03-31') as GuadagniTeorici,
                                                  coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-03-01' and t2.data <= '"""+anno+"""-03-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-03-01' and t1.data <= '"""+anno+"""-03-31')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_guadagnoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-03-01' and t1.data <= '"""+anno+"""-03-31'
                        
                        union
                        
                        select '04/APRILE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-04-01' and t2.data <= '"""+anno+"""-04-30') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-04-01' and t1.data <= '"""+anno+"""-04-30') as GuadagniTeorici,
                                                  coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-04-01' and t2.data <= '"""+anno+"""-04-30') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-04-01' and t1.data <= '"""+anno+"""-04-30')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_guadagnoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-04-01' and t1.data <= '"""+anno+"""-04-30'
                        
                        union
                        
                        select '05/MAGGIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-05-01' and t2.data <= '"""+anno+"""-05-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-05-01' and t1.data <= '"""+anno+"""-05-31') as GuadagniTeorici,
                                                  coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-05-01' and t2.data <= '"""+anno+"""-05-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-05-01' and t1.data <= '"""+anno+"""-05-31')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_guadagnoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-05-01' and t1.data <= '"""+anno+"""-05-31'
                        
                        union
                        
                        select '06/GIUGNO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-06-01' and t2.data <= '"""+anno+"""-06-30') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-06-01' and t1.data <= '"""+anno+"""-06-30') as GuadagniTeorici,
                                                  coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-06-01' and t2.data <= '"""+anno+"""-06-30') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-06-01' and t1.data <= '"""+anno+"""-06-30')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_guadagnoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-06-01' and t1.data <= '"""+anno+"""-06-30'
                        
                        union
                        
                        select '07/LUGLIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-07-01' and t2.data <= '"""+anno+"""-07-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-07-01' and t1.data <= '"""+anno+"""-07-31') as GuadagniTeorici,
                                                  coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-07-01' and t2.data <= '"""+anno+"""-07-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-07-01' and t1.data <= '"""+anno+"""-07-31')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_guadagnoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-07-01' and t1.data <= '"""+anno+"""-07-31'
                        
                        union
                        
                        select '08/AGOSTO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-08-01' and t2.data <= '"""+anno+"""-08-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-08-01' and t1.data <= '"""+anno+"""-08-31') as GuadagniTeorici,
                                                  coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-08-01' and t2.data <= '"""+anno+"""-08-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-08-01' and t1.data <= '"""+anno+"""-08-31')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_guadagnoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-08-01' and t1.data <= '"""+anno+"""-08-31'
                        
                        union
                        
                        select '09/SETTEMBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-09-01' and t2.data <= '"""+anno+"""-09-30') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-09-01' and t1.data <= '"""+anno+"""-09-30') as GuadagniTeorici,
                                                  coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-09-01' and t2.data <= '"""+anno+"""-09-30') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-09-01' and t1.data <= '"""+anno+"""-09-30')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_guadagnoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-09-01' and t1.data <= '"""+anno+"""-09-30'
                        
                        union
                        
                        select '10/OTTOBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-10-01' and t2.data <= '"""+anno+"""-10-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-10-01' and t1.data <= '"""+anno+"""-10-31') as GuadagniTeorici,
                                                  coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-10-01' and t2.data <= '"""+anno+"""-10-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-10-01' and t1.data <= '"""+anno+"""-10-31')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_guadagnoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-10-01' and t1.data <= '"""+anno+"""-10-31'
                        
                        union
                        
                        select '11/NOVEMBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-11-01' and t2.data <= '"""+anno+"""-11-30') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-11-01' and t1.data <= '"""+anno+"""-11-30') as GuadagniTeorici,
                                                  coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-11-01' and t2.data <= '"""+anno+"""-11-30') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-11-01' and t1.data <= '"""+anno+"""-11-30')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_guadagnoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-11-01' and t1.data <= '"""+anno+"""-11-30'
                        
                        union
                        
                        select '12/DICEMBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-12-01' and t2.data <= '"""+anno+"""-12-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-12-01' and t1.data <= '"""+anno+"""-12-31') as GuadagniTeorici,
                                                  coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where t2.data >= '"""+anno+"""-12-01' and t2.data <= '"""+anno+"""-12-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-12-01' and t1.data <= '"""+anno+"""-12-31')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_guadagnoeffettivo t1
                        
                        Where t1.data >= '2018-12-01' and t1.data <= '2018-12-31'
                        
                        union
                        
                        select 'TOTALE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 Where t2.data >= '"""+anno+"""-01-01' and t2.data <= '"""+anno+"""-12-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 Where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-12-31') as GuadagniTeorici,
                                                  coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 Where t2.data >= '"""+anno+"""-01-01' and t2.data <= '"""+anno+"""-12-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 Where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-12-31')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_guadagnoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-12-31'	  
                        
                        ORDER BY mese ASC;"""

            print(query)
            cursor = connection.cursor()
            cursor.execute(query);
            rows = cursor.fetchall()
            print(rows)

            context = {'form': form, 'tabella_output3': rows}
            return render(request, "GestioneGuadagniEffettivi.html", context)




    else:

        rows = []
        form = formGestioneGuadagniEffettivi()
        context = {'form': form, 'tabella_output3': rows}
        return render(request, "GestioneGuadagniEffettivi.html", context)


def viewContabilitaProtocolli(request):
    query = """SELECT t1.identificativo, t1.cliente,t1.indirizzo,t1.pratica,t1.parcella,(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id) as entrate,
                                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as uscite,
                                            t1.parcella-(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id)+
                                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as saldo
                FROM   Contabilita_protocollo t1
                
                union
                
                SELECT t1.identificativo, t1.cliente,t1.indirizzo,t1.pratica,t1.parcella,(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id) as entrate,
                                                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as uscite,
                                                            t1.parcella-(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id)+
                                                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as saldo
                FROM   Contabilita_protocollo t1"""

    print(query)
    cursor = connection.cursor()
    cursor.execute(query);
    rows = cursor.fetchall()
    print(rows)

    context = {'tabella_output4': rows}
    return render(request, "ContabilitaProtocolli.html", context)
