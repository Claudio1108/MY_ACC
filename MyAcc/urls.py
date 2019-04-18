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


urlpatterns = [

    path('admin/', admin.site.urls),

    #Protocollo
    path('HomePage', contviews.viewhomepage, name='HomePage'),
    path('AllProtocols/', contviews.viewAllProtocols, name='AllProtocols'),
    path('CreateProtocol/', contviews.viewCreateProtocol, name='CreateProtocol'),
    path('DeleteProtocol/<int:id>', contviews.viewDeleteProtocol, name='DeleteProtocol'),
    path('UpdateProtocol/<int:id>', contviews.viewUpdateProtocol, name='UpdateProtocol'),
    #Guadagno
    path('AllGuadagni/', contviews.viewAllGuadagni, name='AllGuadagni'),
    path('CreateGuadagno/', contviews.viewCreateGuadagno, name='CreateGuadagno'),
    path('DeleteGuadagno/<int:id>', contviews.viewDeleteGuadagno, name='DeleteGuadagno'),
    path('UpdateGuadagno/<int:id>', contviews.viewUpdateGuadagno, name='UpdateGuadagno'),
    #SpesaCommessa
    path('AllSpeseCommessa/', contviews.viewAllSpeseCommessa, name='AllSpeseCommessa'),
    path('CreateSpesaCommessa/', contviews.viewCreateSpesaCommessa, name='CreateSpesaCommessa'),
    path('DeleteSpesaCommessa/<int:id>', contviews.viewDeleteSpesaCommessa, name='DeleteSpesaCommessa'),
    path('UpdateSpesaCommessa/<int:id>', contviews.viewUpdateSpesaCommessa, name='UpdateSpesaCommessa'),
    #Socio
    path('AllSoci/', contviews.viewAllSoci, name='AllSoci'),
    path('UpdateSocio/<int:id>', contviews.viewUpdateSocio, name='UpdateSocio'),
    #SpeseGestione
    path('AllSpeseGestione/', contviews.viewAllSpeseGestione, name='AllSpeseGestione'),
    path('CreateSpesaGestione/', contviews.viewCreateSpesaGestione, name='CreateSpesaGestione'),
    path('DeleteSpesaGestione/<int:id>', contviews.viewDeleteSpesaGestione, name='DeleteSpesaGestione'),
    path('UpdateSpesaGestione/<int:id>', contviews.viewUpdateSpesaGestione, name='UpdateSpesaGestione'),
    #RicaviEffettivi
    path('AllRIcaviEffettivi/', contviews.viewAllRicaviEffettivi, name='AllRicaviEffettivi'),
    path('CreateRicavoEffettivo/', contviews.viewCreateRicavoEffettivo, name='CreateRicavoEffettivo'),
    path('DeleteRicavoEffettivo/<int:id>', contviews.viewDeleteRicavoEffettivo, name='DeleteRicavoEffettivo'),
    path('UpdateRicavoEffettivo/<int:id>', contviews.viewUpdateRicavoEffettivo, name='UpdateRicavoEffettivo'),

    #Output
    path('ResocontoSpeseGestione/', contviews.viewResocontoSpeseGestione, name='ResocontoSpeseGestione'),
    path('ResocontoGuadagni/', contviews.viewResocontoGuadagni, name='ResocontoGuadagni'),
    path('GestioneRicavi/', contviews.viewGestioneRicavi, name='GestioneRicavi'),
    path('ContabilitaProtocolli/', contviews.viewContabilitaProtocolli, name='ContabilitaProtocolli'),

]
