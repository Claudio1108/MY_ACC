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

    protocollo_filter = ProtocolloFilter(request.GET, queryset=protocolli)

    context = {'filter': protocollo_filter}

    return render(request, "Protocollo/AllProtocols.html", context)

def viewCreateProtocol(request):

    if(request.method == "POST"):

        #creiamo l'istanza del form e la popoliamo con i dati della POST request ("processo di binding")

        form = formProtocol(request.POST)

        if(form.is_valid()):

            print("il form è valido")
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


def viewAllGuadagni(request):

    guadagni = Guadagno.objects.all()

    guadagno_filter = GuadagnoFilter(request.GET, queryset=guadagni)

    context = {'filter': guadagno_filter}

    return render(request, "Guadagno/AllGuadagni.html", context)


def viewCreateGuadagno(request):

    if(request.method == "POST"):

        #creiamo l'istanza del form e la popoliamo con i dati della POST request ("processo di binding")

        form = formGuadagno(request.POST)
        if(form.is_valid()):
            print("il form è valido")
            if(form.Check1()==True):
                form.save()
            else:
                messages.error(request, 'ATTENZIONE. Il Guadagno inserito non rispetta i vincoli di parcella del protocollo')
            return redirect('AllGuadagni')

        else:
            return redirect('AllGuadagni')

    else:

        form = formGuadagno()

        context={'form':form}

        return render(request,"Guadagno/CreateGuadagno.html",context)


def viewDeleteGuadagno(request,id):

    guadagno = Guadagno.objects.get(id=id)
    guadagno.delete()
    return redirect('AllGuadagni')

def viewUpdateGuadagno(request,id):
    if (request.method == "POST"):

        # creiamo l'istanza del form e la popoliamo con i dati della POST request ("processo di binding")
        guadagno = Guadagno.objects.get(id=id)
        form = formGuadagnoUpdate(request.POST, instance=guadagno)

        if (form.is_valid()):
            print("il form è valido")
            if (form.Check1() == True):
                form.save()
            else:
                messages.error(request,
                               'ATTENZIONE. Il Guadagno inserito non rispetta i vincoli di parcella del protocollo')
            return redirect('AllGuadagni')

        else:
            return redirect('AllGuadagni')

    else:
        guadagno = Guadagno.objects.get(id=id)
        form = formGuadagnoUpdate(instance=guadagno)
        context = {'form': form}
        return render(request, "Guadagno/UpdateGuadagno.html", context)


def viewAllSpeseCommessa(request):

    spesecommessa = SpesaCommessa.objects.all()

    context = { "tabella_spesecommessa" : spesecommessa }

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

    context = {'filter': spesagestione_filter}

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

def viewAllRicaviEffettivi(request):

    ricavieffettivi = RicavoEffettivo.objects.all()

    context = { "tabella_ricavieffettivi" : ricavieffettivi }

    return render(request, "RicavoEffettivo/AllRicaviEffettivi.html", context)


def viewCreateRicavoEffettivo(request):

    if(request.method == "POST"):

        #creiamo l'istanza del form e la popoliamo con i dati della POST request ("processo di binding")

        form = formRicavoEffettivo(request.POST)
        if(form.is_valid()):
            print("il form è valido")
            form.save()
            return redirect('AllRicaviEffettivi')

    else:

        form = formRicavoEffettivo()

        context={'form':form}

        return render(request,"RicavoEffettivo/CreateRicavoEffettivo.html",context)

def viewDeleteRicavoEffettivo(request,id):

    ricavoefettivo = RicavoEffettivo.objects.get(id=id)
    ricavoefettivo.delete()
    return redirect('AllRicaviEffettivi')

def viewUpdateRicavoEffettivo(request,id):

    if (request.method == "POST"):

        # creiamo l'istanza del form e la popoliamo con i dati della POST request ("processo di binding")
        ricavoeffettivo = RicavoEffettivo.objects.get(id=id)
        form = formRicavoEffettivoUpdate(request.POST, instance=ricavoeffettivo)

        if (form.is_valid()):
            print("il form è valido")
            form.save()
            return redirect('AllRicaviEffettivi')

    else:
        ricavoeffettivo = RicavoEffettivo.objects.get(id=id)
        form = formRicavoEffettivoUpdate(instance=ricavoeffettivo)
        context = {'form': form}
        return render(request, "RicavoEffettivo/UpdateRicavoEffettivo.html", context)


def viewResocontoSpeseGestione(request):

    if (request.method == "POST"):

        form = formResocontoSpeseGestione(request.POST)

        if (form.is_valid()):
            anno=str(form['year'].value())
            print(anno)
            print(type(anno))

            query="""select '01/GENNAIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-01-31' 
                    UNION
                    select '02/FEBBRAIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-02-01' and t1.data <= '"""+anno+"""-02-28' 
                    UNION
                    select '03/MARZO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-03-01' and t1.data <= '"""+anno+"""-03-31'
                    UNION
                    select '04/APRILE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-04-01' and t1.data <= '"""+anno+"""-04-30' 
                    UNION
                    select '05/MAGGIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-05-01' and t1.data <= '"""+anno+"""-05-31' 
                    UNION
                    select '06/GIUGNO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-06-01' and t1.data <= '"""+anno+"""-06-30' 
                    UNION
                    select '07/LUGLIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-07-01' and t1.data <= '"""+anno+"""-07-31' 
                    UNION
                    select '08/AGOSTO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-08-01' and t1.data <= '"""+anno+"""-08-31' 
                    UNION
                    select '09/SETTEMBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-09-01' and t1.data <= '"""+anno+"""-09-30' 
                    UNION
                    select '10/OTTOBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-10-01' and t1.data <= '"""+anno+"""-10-31' 
                    UNION
                    select '11/NOVEMBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-11-01' and t1.data <= '"""+anno+"""-11-30' 
                    UNION
                    select '12/DICEMBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_spesagestione t1  
                    where t1.data >= '"""+anno+"""-12-01' and t1.data <= '"""+anno+"""-12-31'
                    UNION
                    select 'TOTALE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
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


def viewResocontoGuadagni(request):

    if (request.method == "POST"):

        form = formResocontoGuadagni(request.POST)

        if (form.is_valid()):
            anno=str(form['year'].value())
            print(anno)
            print(type(anno))

            query="""select '01/GENNAIO' as mese, coalesce(sum(t1.importo),0) as guadagno, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico
                    from Contabilita_guadagno t1  
                    where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-01-31' 
                    
                    union
                    
                    select '02/FEBBRAIO' as mese, coalesce(sum(t1.importo),0) as guadagno, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_guadagno t1  
                    where t1.data >= '"""+anno+"""-02-01' and t1.data <= '"""+anno+"""-02-28' 
                    
                    union
                    
                    select '03/MARZO' as mese, coalesce(sum(t1.importo),0) as guadagno, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_guadagno t1  
                    where t1.data >= '"""+anno+"""-03-01' and t1.data <= '"""+anno+"""-03-31' 
                    
                    union
                    
                    select '04/APRILE' as mese, coalesce(sum(t1.importo),0) as guadagno, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_guadagno t1
                    where t1.data >= '"""+anno+"""-04-01' and t1.data <= '"""+anno+"""-04-30' 
                    
                    union
                    
                    select '05/MAGGIO' as mese, coalesce(sum(t1.importo),0) as guadagno, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_guadagno t1
                    where t1.data >= '"""+anno+"""-05-01' and t1.data <= '"""+anno+"""-05-31' 
                    
                    union
                    
                    select '06/GIUGNO' as mese, coalesce(sum(t1.importo),0) as guadagno, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_guadagno t1
                    where t1.data >= '"""+anno+"""-06-01' and t1.data <= '"""+anno+"""-06-30' 
                    
                    union
                    
                    select '07/LUGLIO' as mese, coalesce(sum(t1.importo),0) as guadagno, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_guadagno t1
                    where t1.data >= '"""+anno+"""-07-01' and t1.data <= '"""+anno+"""-07-31' 
                    
                    union
                    
                    select '08/AGOSTO' as mese, coalesce(sum(t1.importo),0) as guadagno, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_guadagno t1
                    where t1.data >= '"""+anno+"""-08-01' and t1.data <= '"""+anno+"""-08-31' 
                    
                    union
                    
                    select '09/SETTEMBRE' as mese, coalesce(sum(t1.importo),0) as guadagno, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_guadagno t1
                    where t1.data >= '"""+anno+"""-09-01' and t1.data <= '"""+anno+"""-09-30' 
                    
                    union
                    
                    select '10/OTTOBRE' as mese, coalesce(sum(t1.importo),0) as guadagno, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_guadagno t1
                    where t1.data >= '"""+anno+"""-10-01' and t1.data <= '"""+anno+"""-10-31' 
                    
                    union
                    
                    select '11/NOVEMBRE' as mese, coalesce(sum(t1.importo),0) as guadagno, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_guadagno t1
                    where t1.data >= '"""+anno+"""-11-01' and t1.data <= '"""+anno+"""-11-30' 
                    
                    union
                    
                    select '12/DICEMBRE' as mese, coalesce(sum(t1.importo),0) as guadagno, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_guadagno t1
                    where t1.data >= '"""+anno+"""-12-01' and t1.data <= '"""+anno+"""-12-31' 
                    
                    union
                    
                    select 'TOTALE' as mese, coalesce(sum(t1.importo),0) as guadagno, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico  
                    from Contabilita_guadagno t1
                    where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-12-31'
                    
                    ORDER BY mese ASC;"""

            print(query)
            cursor = connection.cursor()
            cursor.execute(query);
            rows = cursor.fetchall()
            print(rows)

            context = {'form': form, 'tabella_output2':rows}
            return render(request, "ResocontoGuadagni.html", context)




    else:

        rows=[]
        form = formResocontoGuadagni()
        context = {'form': form, 'tabella_output2':rows}
        return render(request, "ResocontoGuadagni.html", context)

def viewGestioneRicavi(request):
    if (request.method == "POST"):

        form = formGestioneRicavi(request.POST)

        if (form.is_valid()):
            anno = str(form['year'].value())
            print(anno)
            print(type(anno))

            query = """select '01/GENNAIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-01-01' and t2.data <= '"""+anno+"""-01-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-01-31') as RicaviTeorici,
                                                  coalesce(sum(t1.importo),0) as RE, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-01-01' and t2.data <= '"""+anno+"""-01-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-01-31')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_ricavoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-01-31'
                        
                        union
                        
                        select '02/FEBBRAIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-02-01' and t2.data <= '"""+anno+"""-02-28') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-02-01' and t1.data <= '"""+anno+"""-02-28') as RicaviTeorici,
                                                  coalesce(sum(t1.importo),0) as RE, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-02-01' and t2.data <= '"""+anno+"""-02-28') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-02-01' and t1.data <= '"""+anno+"""-02-28')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_ricavoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-02-01' and t1.data <= '"""+anno+"""-02-28'
                        
                        union
                        
                        select '03/MARZO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-03-01' and t2.data <= '"""+anno+"""-03-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-03-01' and t1.data <= '"""+anno+"""-03-31') as RicaviTeorici,
                                                  coalesce(sum(t1.importo),0) as RE, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-03-01' and t2.data <= '"""+anno+"""-03-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-03-01' and t1.data <= '"""+anno+"""-03-31')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_ricavoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-03-01' and t1.data <= '"""+anno+"""-03-31'
                        
                        union
                        
                        select '04/APRILE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-04-01' and t2.data <= '"""+anno+"""-04-30') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-04-01' and t1.data <= '"""+anno+"""-04-30') as RicaviTeorici,
                                                  coalesce(sum(t1.importo),0) as RE, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-04-01' and t2.data <= '"""+anno+"""-04-30') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-04-01' and t1.data <= '"""+anno+"""-04-30')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_ricavoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-04-01' and t1.data <= '"""+anno+"""-04-30'
                        
                        union
                        
                        select '05/MAGGIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-05-01' and t2.data <= '"""+anno+"""-05-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-05-01' and t1.data <= '"""+anno+"""-05-31') as RicaviTeorici,
                                                  coalesce(sum(t1.importo),0) as RE, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-05-01' and t2.data <= '"""+anno+"""-05-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-05-01' and t1.data <= '"""+anno+"""-05-31')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_ricavoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-05-01' and t1.data <= '"""+anno+"""-05-31'
                        
                        union
                        
                        select '06/GIUGNO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-06-01' and t2.data <= '"""+anno+"""-06-30') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-06-01' and t1.data <= '"""+anno+"""-06-30') as RicaviTeorici,
                                                  coalesce(sum(t1.importo),0) as RE, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-06-01' and t2.data <= '"""+anno+"""-06-30') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-06-01' and t1.data <= '"""+anno+"""-06-30')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_ricavoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-06-01' and t1.data <= '"""+anno+"""-06-30'
                        
                        union
                        
                        select '07/LUGLIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-07-01' and t2.data <= '"""+anno+"""-07-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-07-01' and t1.data <= '"""+anno+"""-07-31') as RicaviTeorici,
                                                  coalesce(sum(t1.importo),0) as RE, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-07-01' and t2.data <= '"""+anno+"""-07-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-07-01' and t1.data <= '"""+anno+"""-07-31')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_ricavoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-07-01' and t1.data <= '"""+anno+"""-07-31'
                        
                        union
                        
                        select '08/AGOSTO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-08-01' and t2.data <= '"""+anno+"""-08-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-08-01' and t1.data <= '"""+anno+"""-08-31') as RicaviTeorici,
                                                  coalesce(sum(t1.importo),0) as RE, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-08-01' and t2.data <= '"""+anno+"""-08-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-08-01' and t1.data <= '"""+anno+"""-08-31')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_ricavoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-08-01' and t1.data <= '"""+anno+"""-08-31'
                        
                        union
                        
                        select '09/SETTEMBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-09-01' and t2.data <= '"""+anno+"""-09-30') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-09-01' and t1.data <= '"""+anno+"""-09-30') as RicaviTeorici,
                                                  coalesce(sum(t1.importo),0) as RE, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-09-01' and t2.data <= '"""+anno+"""-09-30') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-09-01' and t1.data <= '"""+anno+"""-09-30')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_ricavoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-09-01' and t1.data <= '"""+anno+"""-09-30'
                        
                        union
                        
                        select '10/OTTOBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-10-01' and t2.data <= '"""+anno+"""-10-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-10-01' and t1.data <= '"""+anno+"""-10-31') as RicaviTeorici,
                                                  coalesce(sum(t1.importo),0) as RE, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-10-01' and t2.data <= '"""+anno+"""-10-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-10-01' and t1.data <= '"""+anno+"""-10-31')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_ricavoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-10-01' and t1.data <= '"""+anno+"""-10-31'
                        
                        union
                        
                        select '11/NOVEMBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-11-01' and t2.data <= '"""+anno+"""-11-30') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-11-01' and t1.data <= '"""+anno+"""-11-30') as RicaviTeorici,
                                                  coalesce(sum(t1.importo),0) as RE, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-11-01' and t2.data <= '"""+anno+"""-11-30') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-11-01' and t1.data <= '"""+anno+"""-11-30')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_ricavoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-11-01' and t1.data <= '"""+anno+"""-11-30'
                        
                        union
                        
                        select '12/DICEMBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-12-01' and t2.data <= '"""+anno+"""-12-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-12-01' and t1.data <= '"""+anno+"""-12-31') as RicaviTeorici,
                                                  coalesce(sum(t1.importo),0) as RE, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 where t2.data >= '"""+anno+"""-12-01' and t2.data <= '"""+anno+"""-12-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where t1.data >= '"""+anno+"""-12-01' and t1.data <= '"""+anno+"""-12-31')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_ricavoeffettivo t1
                        
                        Where t1.data >= '2018-12-01' and t1.data <= '2018-12-31'
                        
                        union
                        
                        select 'TOTALE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 Where t2.data >= '"""+anno+"""-01-01' and t2.data <= '"""+anno+"""-12-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 Where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-12-31') as RicaviTeorici,
                                                  coalesce(sum(t1.importo),0) as RE, coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele') as Daniele , coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura') as Laura,coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico') as Federico,
                                                  (select coalesce(sum(t2.importo),0) from Contabilita_guadagno t2 Where t2.data >= '"""+anno+"""-01-01' and t2.data <= '"""+anno+"""-12-31') -
                                                  (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 Where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-12-31')-coalesce(sum(t1.importo),0) as DIfferenza
                        from Contabilita_ricavoeffettivo t1
                        
                        Where t1.data >= '"""+anno+"""-01-01' and t1.data <= '"""+anno+"""-12-31'	  
                        
                        ORDER BY mese ASC;"""

            print(query)
            cursor = connection.cursor()
            cursor.execute(query);
            rows = cursor.fetchall()
            print(rows)

            context = {'form': form, 'tabella_output3': rows}
            return render(request, "GestioneRicavi.html", context)




    else:

        rows = []
        form = formGestioneRicavi()
        context = {'form': form, 'tabella_output3': rows}
        return render(request, "GestioneRicavi.html", context)


def viewContabilitaProtocolli(request):
    query = """SELECT t1.identificativo, t1.cliente,t1.indirizzo,t1.pratica,t1.parcella,(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_guadagno t2 WHERE t1.id = t2.protocollo_id) as entrate,
                                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as uscite,
                                            t1.parcella-(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_guadagno t2 WHERE t1.id = t2.protocollo_id)+
                                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as saldo
                FROM   Contabilita_protocollo t1
                
                union
                
                SELECT t1.identificativo, t1.cliente,t1.indirizzo,t1.pratica,t1.parcella,(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_guadagno t2 WHERE t1.id = t2.protocollo_id) as entrate,
                                                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as uscite,
                                                            t1.parcella-(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_guadagno t2 WHERE t1.id = t2.protocollo_id)+
                                                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as saldo
                FROM   Contabilita_protocollo t1"""

    print(query)
    cursor = connection.cursor()
    cursor.execute(query);
    rows = cursor.fetchall()
    print(rows)

    context = {'tabella_output4': rows}
    return render(request, "ContabilitaProtocolli.html", context)
