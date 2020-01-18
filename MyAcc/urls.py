"""MyAccounting URL Configuration """
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from Contabilita import views as contviews
from django.conf.urls import url
from Contabilita.views import ProtocolloAutocomplete, ClienteAutocomplete, ReferenteAutocomplete

urlpatterns = [
    path("admin/", admin.site.urls),
    url(r"^favicon\.ico$", RedirectView.as_view(url="/static/images/favicon.ico")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("HomePage", contviews.viewHomePage, name="HomePage"),
    path("HomePageContabilita", contviews.viewHomePageContabilita, name="HomePageContabilita"),
    path(
        "HomePageAmministrazione",
        contviews.viewHomePageAmministrazione,
        name="HomePageAmministrazione",
    ),
    # Cliente
    path("AllClienti/", contviews.viewAllClienti, name="AllClienti"),
    path("CreateCliente/", contviews.viewCreateCliente, name="CreateCliente"),
    path("DeleteCliente/<int:id>", contviews.viewDeleteCliente, name="DeleteCliente"),
    url(r"^DeleteClientiGroup/$", contviews.viewDeleteClientiGroup, name="DeleteClientiGroup"),
    path("UpdateCliente/<int:id>", contviews.viewUpdateCliente, name="UpdateCliente"),
    # Referente
    path("AllReferenti/", contviews.viewAllReferenti, name="AllReferenti"),
    path("CreateReferente/", contviews.viewCreateReferente, name="CreateReferente"),
    path("DeleteReferente/<int:id>", contviews.viewDeleteReferente, name="DeleteReferente"),
    url(
        r"^DeleteReferentiGroup/$", contviews.viewDeleteReferentiGroup, name="DeleteReferentiGroup"
    ),
    path("UpdateReferente/<int:id>", contviews.viewUpdateReferente, name="UpdateReferente"),
    # Protocollo
    path("AllProtocols/", contviews.viewAllProtocols, name="AllProtocols"),
    path("CreateProtocol/", contviews.viewCreateProtocol, name="CreateProtocol"),
    path("DeleteProtocol/<int:id>", contviews.viewDeleteProtocol, name="DeleteProtocol"),
    url(
        r"^DeleteProtocolsGroup/$", contviews.viewDeleteProtocolsGroup, name="DeleteProtocolsGroup"
    ),
    path("UpdateProtocol/<int:id>", contviews.viewUpdateProtocol, name="UpdateProtocol"),
    # Consulenze
    path("AllConsulenze/", contviews.viewAllConsulenze, name="AllConsulenze"),
    path("CreateConsulenza/", contviews.viewCreateConsulenza, name="CreateConsulenza"),
    path("DeleteConsulenza/<int:id>", contviews.viewDeleteConsulenza, name="DeleteConsulenza"),
    url(
        r"^DeleteConsulenzeGroup/$",
        contviews.viewDeleteConsulenzeGroup,
        name="DeleteConsulenzeGroup",
    ),
    path("UpdateConsulenza/<int:id>", contviews.viewUpdateConsulenza, name="UpdateConsulenza"),
    # Ricavo
    path("AllRicavi/", contviews.viewAllRicavi, name="AllRicavi"),
    path("CreateRicavo/", contviews.viewCreateRicavo, name="CreateRicavo"),
    path("DeleteRicavo/<int:id>", contviews.viewDeleteRicavo, name="DeleteRicavo"),
    url(r"^DeleteRicaviGroup/$", contviews.viewDeleteRicaviGroup, name="DeleteRicaviGroup"),
    path("UpdateRicavo/<int:id>", contviews.viewUpdateRicavo, name="UpdateRicavo"),
    # SpesaCommessa
    path("AllSpeseCommessa/", contviews.viewAllSpeseCommessa, name="AllSpeseCommessa"),
    path("CreateSpesaCommessa/", contviews.viewCreateSpesaCommessa, name="CreateSpesaCommessa"),
    path(
        "DeleteSpesaCommessa/<int:id>",
        contviews.viewDeleteSpesaCommessa,
        name="DeleteSpesaCommessa",
    ),
    url(
        r"^DeleteSpeseCommessaGroup/$",
        contviews.viewDeleteSpeseCommessaGroup,
        name="DeleteSpeseCommessaGroup",
    ),
    path(
        "UpdateSpesaCommessa/<int:id>",
        contviews.viewUpdateSpesaCommessa,
        name="UpdateSpesaCommessa",
    ),
    # Socio
    path("AllSoci/", contviews.viewAllSoci, name="AllSoci"),
    path("UpdateSocio/<int:id>", contviews.viewUpdateSocio, name="UpdateSocio"),
    # SpesaGestione
    path("AllSpeseGestione/", contviews.viewAllSpeseGestione, name="AllSpeseGestione"),
    path("CreateSpesaGestione/", contviews.viewCreateSpesaGestione, name="CreateSpesaGestione"),
    path(
        "DeleteSpesaGestione/<int:id>",
        contviews.viewDeleteSpesaGestione,
        name="DeleteSpesaGestione",
    ),
    url(
        r"^DeleteSpeseGestioneGroup/$",
        contviews.viewDeleteSpeseGestioneGroup,
        name="DeleteSpeseGestioneGroup",
    ),
    path(
        "UpdateSpesaGestione/<int:id>",
        contviews.viewUpdateSpesaGestione,
        name="UpdateSpesaGestione",
    ),
    # GuadagnoEffettivo
    path("AllGuadagnoEffettivi/", contviews.viewAllGuadagniEffettivi, name="AllGuadagniEffettivi"),
    path(
        "CreateGuadagnoEffettivo/",
        contviews.viewCreateGuadagnoEffettivo,
        name="CreateGuadagnoEffettivo",
    ),
    path(
        "DeleteGuadagnoEffettivo/<int:id>",
        contviews.viewDeleteGuadagnoEffettivo,
        name="DeleteGuadagnoEffettivo",
    ),
    url(
        r"^DeleteGuadagniEffettiviGroup/$",
        contviews.viewDeleteGuadagniEffettiviGroup,
        name="DeleteGuadagniEffettiviGroup",
    ),
    path(
        "UpdateGuadagnoEffettivo/<int:id>",
        contviews.viewUpdateGuadagnoEffettivo,
        name="UpdateGuadagnoEffettivo",
    ),
    # Output
    path(
        "ResocontoSpeseGestione/",
        contviews.viewResocontoSpeseGestione,
        name="ResocontoSpeseGestione",
    ),
    path("ResocontoRicavi/", contviews.viewResocontoRicavi, name="ResocontoRicavi"),
    path(
        "GestioneGuadagniEffettivi/",
        contviews.viewGestioneGuadagniEffettivi,
        name="GestioneGuadagniEffettivi",
    ),
    path(
        "ContabilitaProtocolli/", contviews.viewContabilitaProtocolli, name="ContabilitaProtocolli"
    ),
    # Reporter
    url(
        r"^export_input_table/xls/\?list=(?P<list>.*)/\?model=(?P<model>.*)$",
        contviews.export_input_table_xls,
        name="export_input_table_xls",
    ),
    url(
        r"^export_output_table/xls/\?numquery=(?P<numquery>.*)/\?year=(?P<year>.*)$",
        contviews.export_output_table_xls,
        name="export_output_table_xls",
    ),
    # Autocompletamento
    url(r"^proto-autocomp/$", ProtocolloAutocomplete.as_view(), name="proto_autocomp"),
    url(r"^cliente-autocomp/$", ClienteAutocomplete.as_view(), name="cliente_autocomp"),
    url(r"^referente-autocomp/$", ReferenteAutocomplete.as_view(), name="referente_autocomp"),
]
