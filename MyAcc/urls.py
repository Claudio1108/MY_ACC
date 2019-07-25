"""MyAccounting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Contabilita import views as contviews
from django.conf.urls import  url


urlpatterns = [

    path('admin/', admin.site.urls),
    #Protocollo
    path('HomePage', contviews.viewhomepage, name='HomePage'),
    #url(r'^AllProtocols/\?order=(?P<order>.*)&csrfmiddlewaretoken=(?P<csrfmiddlewaretoken>.*)$', contviews.viewAllProtocols, name='AllProtocols'),
    path('AllProtocols/', contviews.viewAllProtocols, name='AllProtocols'),
    path('CreateProtocol/', contviews.viewCreateProtocol, name='CreateProtocol'),
    path('DeleteProtocol/<int:id>', contviews.viewDeleteProtocol, name='DeleteProtocol'),
    url(r'^DeleteProtocolsGroup/$', contviews.viewDeleteProtocolsGroup, name='DeleteProtocolsGroup'),
    path('UpdateProtocol/<int:id>', contviews.viewUpdateProtocol, name='UpdateProtocol'),
    #Ricavo
    path('AllRicavi/', contviews.viewAllRicavi, name='AllRicavi'),
    path('CreateRicavo/', contviews.viewCreateRicavo, name='CreateRicavo'),
    path('DeleteRicavo/<int:id>', contviews.viewDeleteRicavo, name='DeleteRicavo'),
    url(r'^DeleteRicaviGroup/$', contviews.viewDeleteRicaviGroup, name='DeleteRicaviGroup'),
    path('UpdateRicavo/<int:id>', contviews.viewUpdateRicavo, name='UpdateRicavo'),
    #SpesaCommessa
    path('AllSpeseCommessa/', contviews.viewAllSpeseCommessa, name='AllSpeseCommessa'),
    path('CreateSpesaCommessa/', contviews.viewCreateSpesaCommessa, name='CreateSpesaCommessa'),
    path('DeleteSpesaCommessa/<int:id>', contviews.viewDeleteSpesaCommessa, name='DeleteSpesaCommessa'),
    url(r'^DeleteSpeseCommessaGroup/$', contviews.viewDeleteSpeseCommessaGroup, name='DeleteSpeseCommessaGroup'),
    path('UpdateSpesaCommessa/<int:id>', contviews.viewUpdateSpesaCommessa, name='UpdateSpesaCommessa'),
    #Socio
    path('AllSoci/', contviews.viewAllSoci, name='AllSoci'),
    path('UpdateSocio/<int:id>', contviews.viewUpdateSocio, name='UpdateSocio'),
    #SpesaGestione
    path('AllSpeseGestione/', contviews.viewAllSpeseGestione, name='AllSpeseGestione'),
    path('CreateSpesaGestione/', contviews.viewCreateSpesaGestione, name='CreateSpesaGestione'),
    path('DeleteSpesaGestione/<int:id>', contviews.viewDeleteSpesaGestione, name='DeleteSpesaGestione'),
    url(r'^DeleteSpeseGestioneGroup/$', contviews.viewDeleteSpeseGestioneGroup, name='DeleteSpeseGestioneGroup'),
    path('UpdateSpesaGestione/<int:id>', contviews.viewUpdateSpesaGestione, name='UpdateSpesaGestione'),
    #GuadagnoEffettivo
    path('AllGuadagnoEffettivi/', contviews.viewAllGuadagniEffettivi, name='AllGuadagniEffettivi'),
    path('CreateGuadagnoEffettivo/', contviews.viewCreateGuadagnoEffettivo, name='CreateGuadagnoEffettivo'),
    path('DeleteGuadagnoEffettivo/<int:id>', contviews.viewDeleteGuadagnoEffettivo, name='DeleteGuadagnoEffettivo'),
    url(r'^DeleteGuadagniEffettiviGroup/$', contviews.viewDeleteGuadagniEffettiviGroup, name='DeleteGuadagniEffettiviGroup'),
    path('UpdateGuadagnoEffettivo/<int:id>', contviews.viewUpdateGuadagnoEffettivo, name='UpdateGuadagnoEffettivo'),

    #Output
    path('ResocontoSpeseGestione/', contviews.viewResocontoSpeseGestione, name='ResocontoSpeseGestione'),
    path('ResocontoRicavi/', contviews.viewResocontoRicavi, name='ResocontoRicavi'),
    path('GestioneGuadagniEffettivi/', contviews.viewGestioneGuadagniEffettivi, name='GestioneGuadagniEffettivi'),
    path('ContabilitaProtocolli/', contviews.viewContabilitaProtocolli, name='ContabilitaProtocolli'),

    #Reporter
    url(r'^export/xls/\?list=(?P<list>.*)/$', contviews.export_protocols_xlsx, name='export_protocols_xlsx')

]
