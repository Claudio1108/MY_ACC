import unicodedata
from datetime import datetime, date
from Contabilita import models

import smtplib, ssl
from email.mime.text import MIMEText


def _string_normalize_unicode(string):
    return unicodedata.normalize('NFD', string).encode('ascii', 'ignore').decode("utf-8")

def send_mail(text):
    gmail_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    gmail_server.ehlo()
    gmail_server.login('alicloudjob@gmail.com', '150219.cal')
    # server_gmail.starttls(context=ssl.create_default_context())

    msg = MIMEText(text)
    msg['Subject'] = '!!!REMINDER!!! Protocolli/Consulenze'
    msg['From'] = 'alicloudjob@gmail.com'
    msg['To'] = 'alicino.claudio@gmail.com'
    gmail_server.sendmail('alicloudjob@gmail.com', 'alicino.claudio@gmail.com', msg.as_string())
    gmail_server.close()


def my_cron_job():
    # f = open('/Users/claudio.alicino/PycharmProjects/MY_ACC/{}.txt'.format(datetime.now().strftime("%d-%m-%Y%H:%M:%S")), 'w')
    lista_protocolli = list()
    for p in models.Protocollo.objects.all():
        diff = (date.today() - p.data_scadenza).days
        if diff >= -3 and p.data_consegna is None:
            lista_protocolli.append((str(diff),
                                     _string_normalize_unicode(str(p.cliente)),
                                     _string_normalize_unicode(str(p.indirizzo)), str(p.pratica),
                                     'SCADUTO' if diff > 0 else 'IN SCADENZA',
                                     datetime.strptime(str(p.data_scadenza), '%Y-%m-%d').strftime('%d/%m/%Y')))
    mail_text = ''
    if lista_protocolli:
        # [('15', 'Ciraco Andrea/3389701302', 'Via Roberto Michels, 12', 'Progetto CILA DOCFA DL', 'SCADUTO', '10/02/2021'),
        # ('-3', 'Camilla/123', 'Via Braccio da Montone, 8', 'APE', 'IN SCADENZA', '28/02/2021')]
        lista_protocolli.sort(reverse=True, key=lambda tup: tup[1])
        mail_text = '\nPROTOCOLLI:\n'+''.join([item[1]+'\t|\t'+item[2]+'\t|\t'+item[3]+'\t|\t'+item[4]+' il '+item[5]+'\n' for item in lista_protocolli])
        # f.writelines(mail_text)

    #  diff >= 1  -->  Red  |  -3 >= diff >= 0  --> Yellow  |  diff <= -4 --> Green
    lista_consulenze = list()
    for c in models.Consulenza.objects.all():
        diff = (date.today() - c.data_scadenza).days
        if diff >= -3 and c.data_consegna is None:
            lista_consulenze.append((str(diff),
                                     _string_normalize_unicode(str(c.richiedente)),
                                     _string_normalize_unicode(str(c.indirizzo)), str(c.attivita),
                                     'SCADUTO' if diff > 0 else 'IN SCADENZA',
                                     datetime.strptime(str(p.data_scadenza), '%Y-%m-%d').strftime('%d/%m/%Y')))
    if lista_consulenze:
        lista_consulenze.sort(reverse=True, key=lambda tup: tup[1])
        mail_text = mail_text+'\nCONSULENZE:\n'+''.join([item[1]+'\t|\t'+item[2]+'\t|\t'+item[3]+'\t|\t'+item[4]+' il '+item[5]+'\n' for item in lista_consulenze])

    if mail_text:
        send_mail(mail_text)

    # f.close()
