from datetime import date, datetime
import re
import xlwt
from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect, render

# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView
from django.utils.decorators import method_decorator

from Contabilita import sqlite_queries as sqlite
from Contabilita import models as contabilita_models
from Contabilita import filters as contabilita_filters
from Contabilita import forms as contabilita_forms


class ProtocolloAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = contabilita_models.Protocollo.objects.all()
        return (
            qs.filter(identificativo__icontains=self.q) | qs.filter(indirizzo__icontains=self.q)
            if self.q
            else qs
        )


class ClienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = contabilita_models.RubricaClienti.objects.all()
        return (
            qs.filter(nominativo__icontains=self.q) | qs.filter(tel__icontains=self.q)
            if self.q
            else qs
        )


class ReferenteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = contabilita_models.RubricaReferenti.objects.all()
        return (
            qs.filter(nominativo__icontains=self.q) | qs.filter(tel__icontains=self.q)
            if self.q
            else qs
        )


# In questo modo abbiamo la funzione da usare nei test che usano la view come funzione
# Inoltre abbiamo anche ridotto ad una linea soltanto la view.
viewHomePage = login_required(TemplateView.as_view(template_name="Homepage/HomePage.html"))

viewHomePageContabilita = login_required(TemplateView.as_view(template_name="Homepage/HomePageContabilita.html"))

viewHomePageAmministrazione = login_required(TemplateView.as_view(template_name="Homepage/HomePageAmministrazione.html"))


"""
Ho provato a migliorare le view dei Clienti relative alle operazioni di: visualizzazione, creazione e modifica
"""

# def viewAllClienti(request):
#     if not request.user.is_authenticated:
#         return redirect("/accounts/login/")
#     else:
#         cliente_filter = contabilita_filters.ClienteFilter(
#             request.GET, queryset=contabilita_models.RubricaClienti.objects.all().order_by("nominativo")
#         )
#         return render(
#             request,
#             "Amministrazione/Cliente/AllClienti.html",
#             {"filter": cliente_filter},
#         )

@method_decorator(login_required, name='dispatch')
class viewAllClienti(ListView):
    model = contabilita_models.RubricaClienti
    template_name = 'Amministrazione/Cliente/AllClienti.html'

    def get_queryset(self):
        return contabilita_filters.ClienteFilter(self.request.GET, queryset=contabilita_models.RubricaClienti.objects.all().order_by("nominativo"))

    def get_context_data(self):
        context = super(viewAllClienti, self).get_context_data()
        context['filter'] = self.get_queryset()
        return context

# class viewAllClienti(ListView):
#     model = contabilita_models.RubricaClienti
#     template_name = 'Amministrazione/Cliente/AllClienti.html'
#     # filterset_class = contabilita_filters.ClienteFilter
#     context_object_name = 'filter'
#
#     def get_queryset(self):
#         return contabilita_filters.ClienteFilter(
#                 self.request.GET, queryset=contabilita_models.RubricaClienti.objects.all().order_by("nominativo")).qs


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#FIRST VERSION CREATE CLIENTE
# def viewCreateCliente(request):
#     if not request.user.is_authenticated:
#         return redirect("/accounts/login/")
#     else:
#         if request.method == "POST":
#             form = formCliente(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect("AllClienti")
#             else:
#                 return render(request, "Amministrazione/Cliente/CreateCliente.html", {"form": form})
#         else:
#             return render(
#                 request, "Amministrazione/Cliente/CreateCliente.html", {"form": formCliente()}
#             )

#SECOND VERSION CREATE CLIENTE
# @method_decorator(login_required, name='dispatch')
# class viewCreateCliente(CreateView):
#     def get(self, request):
#         return render(request, "Amministrazione/Cliente/CreateCliente.html", {"form": contabilita_forms.formCliente()})
#
#     def post(self, request):
#         form = contabilita_forms.formCliente(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("AllClienti")
#         else:
#             return render(request, "Amministrazione/Cliente/CreateCliente.html", {"form": form})

#LAST VERSION CREATE CLIENTE
@method_decorator(login_required, name='dispatch')
class viewCreateCliente(CreateView):
    model = contabilita_models.RubricaClienti
    form_class = contabilita_forms.formCliente
    success_url = reverse_lazy('AllClienti')
    template_name = 'Amministrazione/Cliente/CreateCliente.html'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

"""
Per quanto riguarda la conversione della view relativa alla cancellazione di un Cliente, la documentazione di Django
propone l'utilizzo della classe generica DeleteView la quale per la conferma della cancellazione da parte dell'utente
fa NECESSARIAMENTE affidamento ad una pagina html (rubricaclienti_confirm_delete.html) che dovremmo aggiungere al progetto. 
La conferma della cancellazione è un tema che avevo già risolto da front-end mediante l'utilizzo di un piccolo
banner javascript per la conferma di tale operazione. Come approccio preferisco mantenere il mio, lo trovo più pulito e
meno macchinoso.
"""

def viewDeleteCliente(request, id):
    contabilita_models.RubricaClienti.objects.get(id=id).delete()
    return redirect("AllClienti")

# @method_decorator(login_required, name='dispatch')
# class viewDeleteCliente(DeleteView):
#     model = contabilita_models.RubricaClienti
#     template_name = 'Amministrazione/Cliente/rubricaclienti_confirm_delete.html'
#     success_url = "/AllClienti"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def viewDeleteClientiGroup(request):
    if request.method == "POST":
        for task in request.POST.getlist("list[]"):
            contabilita_models.RubricaClienti.objects.get(id=int(task)).delete()
    return render(request, "Homepage/HomePageAmministrazione.html")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# def viewUpdateCliente(request, id):
#     if not request.user.is_authenticated:
#         return redirect("/accounts/login/")
#     else:
#         if request.method == "POST":
#             form = contabilita_forms.formCliente(request.POST, instance=contabilita_models.RubricaClienti.objects.get(id=id))
#             if form.is_valid():
#                 form.save()
#                 return redirect("AllClienti")
#             else:
#                 return render(request, "Amministrazione/Cliente/UpdateCliente.html", {"form": form})
#         else:
#             return render(
#                 request,
#                 "Amministrazione/Cliente/UpdateCliente.html",
#                 {"form": contabilita_forms.formCliente(instance=contabilita_models.RubricaClienti.objects.get(id=id))},
#             )

@method_decorator(login_required, name='dispatch')
class viewUpdateCliente(UpdateView):
    model = contabilita_models.RubricaClienti
    form_class = contabilita_forms.formCliente
    success_url = reverse_lazy('AllClienti')
    template_name = "Amministrazione/Cliente/UpdateCliente.html"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def viewAllReferenti(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        referente_filter = contabilita_filters.ReferenteFilter(
            request.GET, queryset=contabilita_models.RubricaReferenti.objects.all().order_by("nominativo")
        )
        return render(
            request,
            "Amministrazione/Referente/AllReferenti.html",
            {"filter": referente_filter, "filter_queryset": referente_filter.qs},
        )


def viewCreateReferente(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            form = contabilita_forms.formReferente(request.POST)
            if form.is_valid():
                form.save()
                return redirect("AllReferenti")
            else:
                return render(
                    request, "Amministrazione/Referente/CreateReferente.html", {"form": form}
                )
        else:
            return render(
                request, "Amministrazione/Referente/CreateReferente.html", {"form": contabilita_forms.formReferente()}
            )


def viewDeleteReferente(request, id):
    contabilita_models.RubricaReferenti.objects.get(id=id).delete()
    return redirect("AllReferenti")


def viewDeleteReferentiGroup(request):
    if request.method == "POST":
        for task in request.POST.getlist("list[]"):
            contabilita_models.RubricaReferenti.objects.get(id=int(task)).delete()
    return render(request, "Homepage/HomePageAmministrazione.html")


def viewUpdateReferente(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            form = contabilita_forms.formReferente(request.POST, instance=contabilita_models.RubricaReferenti.objects.get(id=id))
            if form.is_valid():
                form.save()
                return redirect("AllReferenti")
            else:
                return render(
                    request, "Amministrazione/Referente/UpdateReferente.html", {"form": form}
                )
        else:
            return render(
                request,
                "Amministrazione/Referente/UpdateReferente.html",
                {"form": contabilita_forms.formReferente(instance=contabilita_models.RubricaReferenti.objects.get(id=id))},
            )


def viewAllProtocols(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        protocollo_filter = contabilita_filters.ProtocolloFilter(
            request.GET,
            queryset=contabilita_models.Protocollo.objects.all().order_by(
                "-data_registrazione__year", "-identificativo"
            ),
        )
        for proto in protocollo_filter.qs:
            data_scadenza = datetime.strptime(str(proto.data_scadenza), "%Y-%m-%d").date()
            if proto.data_consegna != None:
                proto.status = None
            else:
                proto.status = (data_scadenza - date.today()).days
                contabilita_models.Protocollo.objects.filter(identificativo=proto.identificativo).update(
                    status=proto.status
                )
        sum_parcelle = round(
            protocollo_filter.qs.aggregate(Sum("parcella"))["parcella__sum"] or 0, 2
        )
        return render(
            request,
            "Amministrazione/Protocollo/AllProtocols.html",
            {
                "filter": protocollo_filter,
                "filter_queryset": protocollo_filter.qs,
                "sum_p": sum_parcelle,
            },
        )


def viewCreateProtocol(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            form = contabilita_forms.formProtocol(request.POST)
            anno = form["data_registrazione"].value()[0:4]
            progressive_number_calendar = contabilita_models.CalendarioContatore.objects.filter(id=anno).values(
                "count"
            )[0]["count"]
            contabilita_models.CalendarioContatore.objects.filter(id=anno).update(
                count=str(progressive_number_calendar + 1)
            )
            form.set_identificativo(
                str("{0:03}".format(progressive_number_calendar + 1)) + "-" + anno[2:4]
            )
            data_scadenza = datetime.strptime(form["data_scadenza"].value(), "%Y-%m-%d").date()
            form.set_status(None) if form["data_consegna"].value() != "" else form.set_status(
                (data_scadenza - date.today()).days
            )
            if form.check_date():
                if form.is_valid():
                    form.save()
                    return redirect("AllProtocols")
                else:
                    return render(
                        request, "Amministrazione/Protocollo/CreateProtocol.html", {"form": form}
                    )
            else:
                messages.error(
                    request,
                    "ATTENZIONE! La Data di Scadenza e la Data di Consegna devono essere necessariamente successive o correnti alla Data di Registrazione.",
                )
                return render(
                    request, "Amministrazione/Protocollo/CreateProtocol.html", {"form": form}
                )
        else:
            return render(
                request, "Amministrazione/Protocollo/CreateProtocol.html", {"form": contabilita_forms.formProtocol()}
            )


def viewDeleteProtocol(request, id):
    contabilita_models.Protocollo.objects.get(id=id).delete()
    return redirect("AllProtocols")


def viewDeleteProtocolsGroup(request):
    if request.method == "POST":
        for task in request.POST.getlist("list[]"):
            contabilita_models.Protocollo.objects.get(id=int(task)).delete()
    return render(request, "Homepage/HomePageAmministrazione.html")


def viewUpdateProtocol(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            form = contabilita_forms.formProtocolUpdate(request.POST, instance=contabilita_models.Protocollo.objects.get(id=id))
            anno = form["data_registrazione"].value()[-4:]
            progressive_number_calendar = contabilita_models.CalendarioContatore.objects.filter(id=anno).values(
                "count"
            )[0]["count"]
            if anno != str(contabilita_models.Protocollo.objects.get(id=id).data_registrazione.year):
                contabilita_models.CalendarioContatore.objects.filter(id=anno).update(
                    count=str(progressive_number_calendar + 1)
                )
                form.set_identificativo(
                    str("{0:03}".format(progressive_number_calendar + 1)) + "-" + anno[2:4]
                )
            data_scadenza = datetime.strptime(form["data_scadenza"].value(), "%d/%m/%Y").date()
            form.set_status(None) if form["data_consegna"].value() != "" else form.set_status(
                (data_scadenza - date.today()).days
            )
            if form.check_date():
                if form.is_valid():
                    form.save()
                    anno != str(
                        contabilita_models.Protocollo.objects.get(id=id).data_registrazione.year
                    ) and contabilita_models.Protocollo.objects.filter(id=id).update(
                        identificativo=str("{0:03}".format(progressive_number_calendar + 1))
                        + "-"
                        + anno[2:4]
                    )
                    return redirect("AllProtocols")
                else:
                    return render(
                        request, "Amministrazione/Protocollo/UpdateProtocol.html", {"form": form}
                    )
            else:
                messages.error(
                    request,
                    "ATTENZIONE! La Data di Scadenza e la Data di Consegna devono essere necessariamente successive o correnti alla Data di Registrazione.",
                )
                return render(
                    request, "Amministrazione/Protocollo/UpdateProtocol.html", {"form": form}
                )
        else:
            return render(
                request,
                "Amministrazione/Protocollo/UpdateProtocol.html",
                {"form": contabilita_forms.formProtocolUpdate(instance=contabilita_models.Protocollo.objects.get(id=id))},
            )


def viewAllConsulenze(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        consulenza_filter = contabilita_filters.ConsulenzaFilter(
            request.GET, queryset=contabilita_models.Consulenza.objects.all().order_by("-id")
        )
        for cons in consulenza_filter.qs:
            data_scadenza = datetime.strptime(str(cons.data_scadenza), "%Y-%m-%d").date()
            if cons.data_consegna != None:
                cons.status = None
            else:
                cons.status = (data_scadenza - date.today()).days
                contabilita_models.Consulenza.objects.filter(id=cons.id).update(status=cons.status)
        sum_compensi = round(
            consulenza_filter.qs.aggregate(Sum("compenso"))["compenso__sum"] or 0, 2
        )
        return render(
            request,
            "Amministrazione/Consulenza/AllConsulenze.html",
            {
                "filter": consulenza_filter,
                "filter_queryset": consulenza_filter.qs,
                "sum_c": sum_compensi,
            },
        )


def viewCreateConsulenza(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            form = contabilita_forms.formConsulenza(request.POST)
            data_scadenza = datetime.strptime(form["data_scadenza"].value(), "%Y-%m-%d").date()
            form.set_status(None) if form["data_consegna"].value() != "" else form.set_status(
                (data_scadenza - date.today()).days
            )
            if form.check_date():
                if form.is_valid():
                    form.save()
                    return redirect("AllConsulenze")
                else:
                    return render(
                        request, "Amministrazione/Consulenza/CreateConsulenza.html", {"form": form}
                    )
            else:
                messages.error(
                    request,
                    "ATTENZIONE! La Data di Scadenza e la Data di Consegna devono essere necessariamente successive o correnti alla Data di Registrazione.",
                )
                return render(
                    request, "Amministrazione/Consulenza/CreateConsulenza.html", {"form": form}
                )
        else:
            return render(
                request,
                "Amministrazione/Consulenza/CreateConsulenza.html",
                {"form": contabilita_forms.formConsulenza()},
            )


def viewDeleteConsulenza(request, id):
    contabilita_models.Consulenza.objects.get(id=id).delete()
    return redirect("AllConsulenze")


def viewDeleteConsulenzeGroup(request):
    if request.method == "POST":
        for task in request.POST.getlist("list[]"):
            contabilita_models.Consulenza.objects.get(id=int(task)).delete()
    return render(request, "Homepage/HomePageAmministrazione.html")


def viewUpdateConsulenza(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            form = contabilita_forms.formConsulenzaUpdate(request.POST, instance=contabilita_models.Consulenza.objects.get(id=id))
            data_scadenza = datetime.strptime(form["data_scadenza"].value(), "%d/%m/%Y").date()
            form.set_status(None) if form["data_consegna"].value() != "" else form.set_status(
                (data_scadenza - date.today()).days
            )
            if form.check_date():
                if form.is_valid():
                    form.save()
                    return redirect("AllConsulenze")
                else:
                    return render(
                        request, "Amministrazione/Consulenza/UpdateConsulenza.html", {"form": form}
                    )
            else:
                messages.error(
                    request,
                    "ATTENZIONE! La Data di Scadenza e la Data di Consegna devono essere necessariamente successive o correnti alla Data di Registrazione.",
                )
                return render(
                    request, "Amministrazione/Consulenza/UpdateConsulenza.html", {"form": form}
                )
        else:
            return render(
                request,
                "Amministrazione/Consulenza/UpdateConsulenza.html",
                {"form": contabilita_forms.formConsulenzaUpdate(instance=contabilita_models.Consulenza.objects.get(id=id))},
            )


def viewAllRicavi(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        ricavo_filter = contabilita_filters.RicavoFilter(
            request.GET, queryset=contabilita_models.Ricavo.objects.all().order_by("-data_registrazione")
        )
        sum_ricavi_for_proto = [
            (
                r1.id,
                r1.protocollo.parcella
                - sum(r2.importo for r2 in ricavo_filter.qs if r1.protocollo == r2.protocollo),
            )
            if r1.protocollo is not None
            else (r1.id, 0)
            for r1 in ricavo_filter.qs
        ]
        sum_ricavi = round(ricavo_filter.qs.aggregate(Sum("importo"))["importo__sum"] or 0, 2)
        return render(
            request,
            "Contabilita/Ricavo/AllRicavi.html",
            {
                "filter": ricavo_filter,
                "sum_r": sum_ricavi,
                "info": zip(ricavo_filter.qs, sum_ricavi_for_proto),
            },
        )


def viewCreateRicavo(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            form = contabilita_forms.formRicavo(request.POST)
            if form.is_valid():
                if form["protocollo"].value() != "" and not form.Check1():
                    messages.error(
                        request,
                        "ATTENZIONE! Il Ricavo inserito non rispetta i limiti di parcella del protocollo assegnato.",
                    )
                    return render(request, "Contabilita/Ricavo/CreateRicavo.html", {"form": form})
                else:
                    form.save()
                    return redirect("AllRicavi")
            else:
                return render(request, "Contabilita/Ricavo/CreateRicavo.html", {"form": form})
        else:
            return render(request, "Contabilita/Ricavo/CreateRicavo.html", {"form": contabilita_forms.formRicavo()})


def viewDeleteRicavo(request, id):
    contabilita_models.Ricavo.objects.get(id=id).delete()
    return redirect("AllRicavi")


def viewDeleteRicaviGroup(request):
    if request.method == "POST":
        for task in request.POST.getlist("list[]"):
            contabilita_models.Ricavo.objects.get(id=int(task)).delete()
    return render(request, "Homepage/HomePageContabilita.html")


def viewUpdateRicavo(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            ricavo = contabilita_models.Ricavo.objects.get(id=id)
            form = contabilita_forms.formRicavoUpdate(request.POST, instance=ricavo)
            if form.is_valid():
                if form["protocollo"].value() != "" and not form.Check2(ricavo):
                    messages.error(
                        request,
                        "ATTENZIONE! Il Ricavo modificato non rispetta i limiti di parcella del protocollo assegnato.",
                    )
                    return render(request, "Contabilita/Ricavo/UpdateRicavo.html", {"form": form})
                else:
                    form.save()
                    return redirect("AllRicavi")
            else:
                return render(request, "Contabilita/Ricavo/UpdateRicavo.html", {"form": form})
        else:
            return render(
                request,
                "Contabilita/Ricavo/UpdateRicavo.html",
                {"form": contabilita_forms.formRicavoUpdate(instance=contabilita_models.Ricavo.objects.get(id=id))},
            )


def viewAllSpeseCommessa(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        spesacommessa_filter = contabilita_filters.SpesaCommessaFilter(
            request.GET, queryset=contabilita_models.SpesaCommessa.objects.all().order_by("-data_registrazione")
        )
        sum_spesecommessa = round(
            spesacommessa_filter.qs.aggregate(Sum("importo"))["importo__sum"] or 0, 2
        )
        return render(
            request,
            "Contabilita/SpesaCommessa/AllSpeseCommessa.html",
            {
                "filter": spesacommessa_filter,
                "filter_queryset": spesacommessa_filter.qs,
                "sum_s": sum_spesecommessa,
            },
        )


def viewCreateSpesaCommessa(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            form = contabilita_forms.formSpesaCommessa(request.POST)
            if form.is_valid():
                form.save()
                return redirect("AllSpeseCommessa")
            else:
                return render(
                    request, "Contabilita/SpesaCommessa/CreateSpesaCommessa.html", {"form": form}
                )
        else:
            return render(
                request,
                "Contabilita/SpesaCommessa/CreateSpesaCommessa.html",
                {"form": contabilita_forms.formSpesaCommessa()},
            )


def viewDeleteSpesaCommessa(request, id):
    contabilita_models.SpesaCommessa.objects.get(id=id).delete()
    return redirect("AllSpeseCommessa")


def viewDeleteSpeseCommessaGroup(request):
    if request.method == "POST":
        for task in request.POST.getlist("list[]"):
            contabilita_models.SpesaCommessa.objects.get(id=int(task)).delete()
    return render(request, "Homepage/HomePageContabilita.html")


def viewUpdateSpesaCommessa(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            form = contabilita_forms.formSpesaCommessaUpdate(request.POST, instance=contabilita_models.SpesaCommessa.objects.get(id=id))
            if form.is_valid():
                form.save()
                return redirect("AllSpeseCommessa")
            else:
                return render(
                    request, "Contabilita/SpesaCommessa/UpdateSpesaCommessa.html", {"form": form}
                )
        else:
            return render(
                request,
                "Contabilita/SpesaCommessa/UpdateSpesaCommessa.html",
                {"form": contabilita_forms.formSpesaCommessaUpdate(instance=contabilita_models.SpesaCommessa.objects.get(id=id))},
            )


def viewAllSoci(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        saldi = list()
        soci = contabilita_models.Socio.objects.all().order_by("-percentuale")
        for tipo_saldo in ["CARTA", "DEPOSITO"]:
            saldi.append(sqlite.calculate_saldo(tipo_saldo))
        return render(
            request, "Contabilita/Socio/AllSoci.html", {"tabella_soci": soci, "lista_saldi": saldi}
        )


def viewUpdateSocio(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            socio = contabilita_models.Socio.objects.get(id=id)
            form = contabilita_forms.formSocio(request.POST, instance=socio)
            soci = contabilita_models.Socio.objects.all()
            sum_percentuali = sum(soc.percentuale for soc in soci if (soc.id != id))
            if form.is_valid():
                if float(sum_percentuali) + float(form["percentuale"].value()) < 1.00:
                    form.save()
                    messages.warning(request, "Le percentuali non sono distrubuite completamente")
                else:
                    messages.error(request, "ATTENZIONE! Percentuale inserita invalida.") if (
                        float(sum_percentuali) + float(form["percentuale"].value()) > 1.00
                    ) else form.save()
                return redirect("AllSoci")
            else:
                return render(
                    request, "Contabilita/Socio/UpdateSocio.html", {"form": form, "socio": socio}
                )
        else:
            socio = contabilita_models.Socio.objects.get(id=id)
            form = contabilita_forms.formSocio(instance=socio)
            return render(
                request, "Contabilita/Socio/UpdateSocio.html", {"form": form, "socio": socio}
            )


def viewAllSpeseGestione(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        spesagestione_filter = contabilita_filters.SpesaGestioneFilter(
            request.GET, queryset=contabilita_models.SpesaGestione.objects.all().order_by("-data_registrazione")
        )
        sum_spesegestione = round(
            spesagestione_filter.qs.aggregate(Sum("importo"))["importo__sum"] or 0, 2
        )
        return render(
            request,
            "Contabilita/SpesaGestione/AllSpeseGestione.html",
            {
                "filter": spesagestione_filter,
                "filter_queryset": spesagestione_filter.qs,
                "sum_s": sum_spesegestione,
            },
        )


def viewCreateSpesaGestione(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            form = contabilita_forms.contabilita_forms.formSpesaGestione(request.POST)
            if form.is_valid():
                form.save()
                return redirect("AllSpeseGestione")
            else:
                return render(
                    request, "Contabilita/SpesaGestione/CreateSpesaGestione.html", {"form": form}
                )
        else:
            return render(
                request,
                "Contabilita/SpesaGestione/CreateSpesaGestione.html",
                {"form": contabilita_forms.formSpesaGestione()},
            )


def viewDeleteSpesaGestione(request, id):
    contabilita_models.SpesaGestione.objects.get(id=id).delete()
    return redirect("AllSpeseGestione")


def viewDeleteSpeseGestioneGroup(request):
    if request.method == "POST":
        for task in request.POST.getlist("list[]"):
            contabilita_models.SpesaGestione.objects.get(id=int(task)).delete()
    return render(request, "Homepage/HomePageContabilita.html")


def viewUpdateSpesaGestione(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            form = contabilita_forms.formSpesaGestioneUpdate(request.POST, instance=contabilita_models.SpesaGestione.objects.get(id=id))
            if form.is_valid():
                form.save()
                return redirect("AllSpeseGestione")
            else:
                return render(
                    request, "Contabilita/SpesaGestione/UpdateSpesaGestione.html", {"form": form}
                )
        else:
            return render(
                request,
                "Contabilita/SpesaGestione/UpdateSpesaGestione.html",
                {"form": contabilita_forms.formSpesaGestioneUpdate(instance=contabilita_models.SpesaGestione.objects.get(id=id))},
            )


def viewAllGuadagniEffettivi(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        guadagnoeffettivo_filter = contabilita_filters.GuadagnoEffettivoFilter(
            request.GET, queryset=contabilita_models.GuadagnoEffettivo.objects.all().order_by("-data_registrazione")
        )
        sum_guadagnieffettivi = round(
            guadagnoeffettivo_filter.qs.aggregate(Sum("importo"))["importo__sum"] or 0, 2
        )
        return render(
            request,
            "Contabilita/GuadagnoEffettivo/AllGuadagniEffettivi.html",
            {
                "filter": guadagnoeffettivo_filter,
                "filter_queryset": guadagnoeffettivo_filter.qs,
                "sum_g": sum_guadagnieffettivi,
            },
        )


def viewCreateGuadagnoEffettivo(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            form = contabilita_forms.formGuadagnoEffettivo(request.POST)
            if form.is_valid():
                form.save()
                return redirect("AllGuadagniEffettivi")
            else:
                return render(
                    request,
                    "Contabilita/GuadagnoEffettivo/CreateGuadagnoEffettivo.html",
                    {"form": form},
                )
        else:
            return render(
                request,
                "Contabilita/GuadagnoEffettivo/CreateGuadagnoEffettivo.html",
                {"form": contabilita_forms.formGuadagnoEffettivo()},
            )


def viewDeleteGuadagnoEffettivo(request, id):
    contabilita_models.GuadagnoEffettivo.objects.get(id=id).delete()
    return redirect("AllGuadagniEffettivi")


def viewDeleteGuadagniEffettiviGroup(request):
    if request.method == "POST":
        for task in request.POST.getlist("list[]"):
            contabilita_models.GuadagnoEffettivo.objects.get(id=int(task)).delete()
    return render(request, "Homepage/HomePageContabilita.html")


def viewUpdateGuadagnoEffettivo(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            form = contabilita_forms.formGuadagnoEffettivoUpdate(
                request.POST, instance=contabilita_models.GuadagnoEffettivo.objects.get(id=id)
            )
            if form.is_valid():
                form.save()
                return redirect("AllGuadagniEffettivi")
            else:
                return render(
                    request,
                    "Contabilita/GuadagnoEffettivo/UpdateGuadagnoEffettivo.html",
                    {"form": form},
                )
        else:
            return render(
                request,
                "Contabilita/GuadagnoEffettivo/UpdateGuadagnoEffettivo.html",
                {
                    "form": contabilita_forms.formGuadagnoEffettivoUpdate(
                        instance=contabilita_models.GuadagnoEffettivo.objects.get(id=id)
                    )
                },
            )


def viewResocontoSpeseGestione(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            form = contabilita_forms.form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(request.POST)
            if form.is_valid():
                return render(
                    request,
                    "Contabilita/ResocontoSpeseGestione.html",
                    {
                        "form": form,
                        "tabella_output1": sqlite.resoconto_spese_gestione(form["year"].value()),
                        "year": form["year"].value(),
                    },
                )
            else:
                return render(
                    request,
                    "Contabilita/ResocontoSpeseGestione.html",
                    {"form": form, "tabella_output1": []},
                )
        else:
            return render(
                request,
                "Contabilita/ResocontoSpeseGestione.html",
                {
                    "form": contabilita_forms.form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(),
                    "tabella_output1": [],
                },
            )


def viewResocontoRicavi(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            form = contabilita_forms.form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(request.POST)
            if form.is_valid():
                return render(
                    request,
                    "Contabilita/ResocontoRicavi.html",
                    {
                        "form": form,
                        "tabella_output2": sqlite.resoconto_ricavi(form["year"].value()),
                        "year": form["year"].value(),
                    },
                )
            else:
                return render(
                    request,
                    "Contabilita/ResocontoRicavi.html",
                    {"form": form, "tabella_output2": []},
                )
        else:
            return render(
                request,
                "Contabilita/ResocontoRicavi.html",
                {
                    "form": contabilita_forms.form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(),
                    "tabella_output2": [],
                },
            )


def viewGestioneGuadagniEffettivi(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        if request.method == "POST":
            form = contabilita_forms.form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(request.POST)
            if form.is_valid():
                return render(
                    request,
                    "Contabilita/GestioneGuadagniEffettivi.html",
                    {
                        "form": form,
                        "tabella_output3": sqlite.resoconto_guadagni_effettivi(
                            form["year"].value()
                        ),
                        "year": form["year"].value(),
                    },
                )
            else:
                return render(
                    request,
                    "Contabilita/GestioneGuadagniEffettivi.html",
                    {"form": form, "tabella_output3": []},
                )
        else:
            return render(
                request,
                "Contabilita/GestioneGuadagniEffettivi.html",
                {
                    "form": contabilita_forms.form_ResocontoSpeseGestione_Ricavi_GuadagniEffettivi(),
                    "tabella_output3": [],
                },
            )


def viewContabilitaProtocolli(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    else:
        protocols = sqlite.resoconto_contabilita_protocolli()
        return render(
            request,
            "Contabilita/ContabilitaProtocolli.html",
            {"tabella_output4": protocols,
             'tot_saldo': sum([protocol[8] for protocol in protocols])},
        )


def export_input_table_xls(request, list, model):
    fields_models = {
        "protocollo": [
            "Identificativo",
            "Data Registrazione",
            "Nominativo Cliente",
            "Telefono Cliente",
            "Nominativo Referente",
            "Telefono Referente",
            "Indirizzo",
            "Pratica",
            "Parcella",
            "Note",
            "Data Scadenza",
            "Data Consegna",
            "Responsabile",
        ],
        "ricavo": [
            "Data Registrazione",
            "Movimento",
            "Importo",
            "Fattura",
            "Intestatario Fattura",
            "Id Protocollo",
            "Indirizzo Protocollo",
            "Note",
        ],
        "spesacommessa": [
            "Data Registrazione",
            "Importo",
            "Id Protocollo",
            "Indirizzo Protocollo",
            "Note",
        ],
        "spesagestione": ["Data Registrazione", "Importo", "Causale", "Fattura"],
        "guadagnoeffettivo": ["Data Registrazione", "Importo"],
        "consulenza": [
            "Data Registrazione",
            "Richiedente",
            "Indirizzo",
            "Attivita",
            "Compenso",
            "Note",
            "Data Scadenza",
            "Data Consegna",
            "Responsabile",
        ],
        "rubricaclienti": ["Nominativo", "Telefono", "Mail", "Note"],
        "rubricareferenti": ["Nominativo", "Telefono", "Mail", "Note"],
    }
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="{}.xls"'.format(
        request.POST.get("fname")
    )
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet(model)
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = fields_models[model]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    if model == "protocollo":
        rows = contabilita_models.Protocollo.objects.filter(
            identificativo__in=re.findall("(\d+-\d+)", list)
        ).values_list(
            "identificativo",
            "data_registrazione",
            "cliente__nominativo",
            "cliente__tel",
            "referente__nominativo",
            "referente__tel",
            "indirizzo",
            "pratica",
            "parcella",
            "note",
            "data_scadenza",
            "data_consegna",
            "responsabile__cognome",
        )
    if model == "ricavo":
        rows = contabilita_models.Ricavo.objects.filter(id__in=re.findall("(\d+)", list)).values_list(
            "data_registrazione",
            "movimento",
            "importo",
            "fattura",
            "intestatario_fattura__cognome",
            "protocollo__identificativo",
            "protocollo__indirizzo",
            "note",
        )
    if model == "spesacommessa":
        rows = contabilita_models.SpesaCommessa.objects.filter(id__in=re.findall("(\d+)", list)).values_list(
            "data_registrazione",
            "importo",
            "protocollo__identificativo",
            "protocollo__indirizzo",
            "note",
        )
    if model == "spesagestione":
        rows = contabilita_models.SpesaGestione.objects.filter(id__in=re.findall("(\d+)", list)).values_list(
            "data_registrazione", "importo", "causale", "fattura"
        )
    if model == "guadagnoeffettivo":
        rows = contabilita_models.GuadagnoEffettivo.objects.filter(id__in=re.findall("(\d+)", list)).values_list(
            "data_registrazione", "importo"
        )
    if model == "consulenza":
        rows = contabilita_models.Consulenza.objects.filter(id__in=re.findall("(\d+)", list)).values_list(
            "data_registrazione",
            "richiedente",
            "indirizzo",
            "attivita",
            "compenso",
            "note",
            "data_scadenza",
            "data_consegna",
            "responsabile__cognome",
        )
    if model == "rubricaclienti":
        rows = contabilita_models.RubricaClienti.objects.filter(tel__in=re.findall("(\d+)", list)).values_list(
            "nominativo", "tel", "mail", "note"
        )
    if model == "rubricareferenti":
        rows = contabilita_models.RubricaReferenti.objects.filter(tel__in=re.findall("(\d+)", list)).values_list(
            "nominativo", "tel", "mail", "note"
        )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(
                row_num,
                col_num,
                re.sub(r"<[^<]+?>", "", str(row[col_num]).replace("None", "")),
                font_style,
            )
    wb.save(response)
    return response


def export_output_table_xls(request, numquery, year):
    output = ""
    if int(numquery) == 1:
        output = "spese_gestione"
        columns = ["Mese", "Spese di gestione (€)", "Daniele (€)", "Laura (€)", "Federico (€)"]
        rows = sqlite.resoconto_spese_gestione(year)
    if int(numquery) == 2:
        output = "ricavi"
        columns = ["Mese", "Ricavi (€)", "Daniele (€)", "Laura (€)", "Federico (€)"]
        rows = sqlite.resoconto_ricavi(year)
    if int(numquery) == 3:
        output = "guadagni_eff"
        columns = [
            "Mese",
            "Guadagni Teorici (€)",
            "Guadagni Effettivi (€)",
            "Daniele (€)",
            "Laura (€)",
            "Federico (€)",
            "GT - GE (€)",
        ]
        rows = sqlite.resoconto_guadagni_effettivi(year)
    if int(numquery) == 4:
        output = "contabilita_protocolli"
        columns = [
            "Identificativo",
            "Cliente",
            "Referente",
            "Indirizzo",
            "Pratica",
            "Parcella",
            "Entrate",
            "Uscite",
            "Saldo",
        ]
        rows = sqlite.resoconto_contabilita_protocolli()
    wb = xlwt.Workbook(encoding="utf-8")
    if year == "no":
        name_file = request.POST.get("fname")
        ws = wb.add_sheet(output)
    elif year:
        name_file = request.POST.get("fname") + "_" + year
        ws = wb.add_sheet(output + "_" + year)
    else:
        name_file = request.POST.get("fname") + "_YearNotSpecified"
        ws = wb.add_sheet(output + "_YearNotSpecified")
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="{}.xls"'.format(name_file)
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]).replace("None", ""), font_style)
    wb.save(response)
    return response
