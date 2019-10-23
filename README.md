# MY_ACC
=============

MY_ACC è un software per la gestione amministrativa e della contabilità di uno studio tecnico di architettura denominato "STUDIO DOA". Il software è stato realizzato con Django, un framework Python dedicato allo sviluppo di applicazioni web.

Feature
-------

Gli spider disponibili per il crawling sono:

 - idealista: effettua lo scraping su idealista
 - subito: effettua lo scraping su subito
 - kijiji: effettua lo scraping su kijiji
 - bakeca: effettua lo scraping su bakeca

Technologies
------------

La versione di Python utilizzata è la 3.6. La versione di Django utilizzata è la 2.2.3.

Il packet manager utilzzato è pip.

Lo spider si appoggia a mongodb come database per immagazzinare i dati e ad elasticsearch per la standardizzazione dei dati geografici (in particolare per l'aggiunta del codice Istat).

E' fortemente raccomandato l'utilizzo di virtualenv.

Installation
------------

L'installazione prevede la creazione di un virtualenv per mantenere l'ambiente in cui devono girare gli script isolato, con l'installazione delle librerie necessarie attraverso il file dei requirements.txt.

- cd {project\_path}
- virtualenv spider_master
- source bin/activate
- pip install -r requirements.txt

Deploy
------

Gli spider vengono packetizzati come egg e deployati su Scrapyd.
La procedura per deployarli è la seguente:

 - cd {project\_path}
 - python setup.py clean --all
 - python setup.py bdist\_egg
 - curl -s http://{scrapyd\_host:scrapy\_port}/addversion.json -F project={spider\_name} -F version={version} -F egg=@{egg\_file}
 - schedule it to scrapyd

Usage
-----

Gli spider verranno sempre avviati attraverso l'orchestrator, che si occupa di distribuire gli url iniziali alle varie istanze dei crawler su scrapyd. Tuttavia gli spider possono essere avviati anche senza passare attraverso l'orchestrator per scopi di test.
In questo caso i comandi da utilizzare sono:

 - idealista: scrapy crawl idealista -s QUEUE\_KEYS='{url}' (e.g. https://www.idealista.it/vendita-case/roma-provincia/)
 - subito: scrapy crawl subito -s START\_URLS='{url}' (e.g. https://www.subito.it/annunci-lombardia/vendita/immobili/, http://www.subito.it/annunci-lazio/vendita/immobili/, http://www.subito.it/annunci-campania/vendita/immobili/)
 - kijiji: scrapy crawl kijiji -s QUEUE\_KEYS='{url}' (e.g. https://www.kijiji.it/case/vendita/annunci-lombardia/)
 - bakeca: scrapy crawl bakeca -s QUEUE\_KEYS='{url}' (e.g. https://www.bakeca.it/annunci/vendita-case/luogo/molise/)

Nel caso ci dovessero essere input multipli questi vanno concatenati con una virgola (e.g. prov1,prov2,prov3).

Gli spider devono essere avviati dalla cartella del progetto.
