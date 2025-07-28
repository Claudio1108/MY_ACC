from django.db import connection

#------------------------- views.py ------------------------
def resoconto(data_inizio, data_fine):
    cursor = connection.cursor()
    query = """
              WITH RECURSIVE mesi(anno_mese) AS (
              SELECT substr(%s, 1, 7)
              UNION ALL
              SELECT substr(date(anno_mese || '-01', '+1 month'), 1, 7)
              FROM mesi
              WHERE date(anno_mese || '-01') < date(%s)
            ),
            dati AS (
              SELECT 
                substr(data_registrazione, 1, 7) AS anno_mese,
                SUM(importo) AS somma_ricavi,
                0 AS somma_spese
              FROM Contabilita_ricavo
              WHERE date(data_registrazione) BETWEEN date(%s) AND date(%s)
              GROUP BY anno_mese
            
              UNION ALL
            
              SELECT 
                substr(data_registrazione, 1, 7) AS anno_mese,
                0 AS somma_ricavi,
                SUM(importo) AS somma_spese
              FROM Contabilita_spesagestione
              WHERE date(data_registrazione) BETWEEN date(%s) AND date(%s)
              GROUP BY anno_mese
            ),
            aggregati AS (
              SELECT 
                anno_mese,
                SUM(somma_ricavi) AS somma_ricavi,
                SUM(somma_spese) AS somma_spese,
                SUM(somma_ricavi) - SUM(somma_spese) AS utile_netto
              FROM dati
              GROUP BY anno_mese
            )
            SELECT 
              m.anno_mese,
              COALESCE(a.somma_ricavi, 0) AS somma_ricavi,
              COALESCE(a.somma_spese, 0) AS somma_spese,
              COALESCE(a.utile_netto, 0) AS utile_netto
            FROM mesi m
            LEFT JOIN aggregati a ON m.anno_mese = a.anno_mese
            ORDER BY m.anno_mese;
        """
    cursor.execute(query, (data_inizio, data_fine, data_inizio, data_fine, data_inizio, data_fine))
    return cursor.fetchall()[:-1]

def resoconto_contabilita_protocolli(filter):
    cursor = connection.cursor()
    cursor.execute(""" SELECT * FROM(SELECT t1.id, t1.identificativo, t4.nominativo as cliente, t1.referente_id, t1.indirizzo,t1.pratica,t1.parcella,(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id) as entrate,
                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as uscite,
                            t1.parcella-(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id)+
                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as saldo
                       FROM   Contabilita_protocollo t1, Contabilita_rubricaclienti t4
                       WHERE saldo != 0 and t1.cliente_id = t4.id and t1.referente_id is NULL
                       union
                       SELECT t1.id, t1.identificativo, t4.nominativo as cliente, t5.nominativo, t1.indirizzo,t1.pratica,t1.parcella,(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id) as entrate,
                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as uscite,
                            t1.parcella-(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id)+
                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as saldo
                       FROM   Contabilita_protocollo t1, Contabilita_rubricaclienti t4, Contabilita_rubricareferenti t5
                       WHERE saldo != 0 and t1.cliente_id = t4.id and t1.referente_id = t5.id
                       ORDER BY t1.identificativo) {filter}""".format(filter= f"WHERE cliente LIKE '{filter}%';" if filter else ''))
    return cursor.fetchall()

def resoconto_fiscale():
    cursor = connection.cursor()
    query = """
        SELECT
            anni.anno,
            ROUND(COALESCE(fatt.totale_fatturato, 0.0), 2) AS totale_fatturato,
            ROUND(COALESCE(tasse.totale_tasse, 0.0), 2) AS totale_tasse,
            ROUND(
                COALESCE(fatt.totale_fatturato, 0.0) - COALESCE(tasse.totale_tasse, 0.0),
                2
            ) AS differenza,
            ROUND(
                CASE
                    WHEN COALESCE(fatt.totale_fatturato, 0.0) = 0 THEN NULL
                    ELSE COALESCE(tasse.totale_tasse, 0.0) / fatt.totale_fatturato
                END,
                2
            ) AS percentuale_tasse_su_fatturato
        FROM (
            SELECT strftime('%Y', data_registrazione) AS anno
            FROM Contabilita_fattura
            UNION
            SELECT CAST(anno AS TEXT) FROM Contabilita_codicetributo
        ) AS anni
        LEFT JOIN (
            SELECT strftime('%Y', data_registrazione) AS anno, SUM(importo) AS totale_fatturato
            FROM Contabilita_fattura
            GROUP BY anno
        ) AS fatt ON fatt.anno = anni.anno
        LEFT JOIN (
            SELECT CAST(anno AS TEXT) AS anno, SUM(COALESCE(debito, 0) - COALESCE(credito, 0)) AS totale_tasse
            FROM Contabilita_codicetributo
            GROUP BY anno
        ) AS tasse ON tasse.anno = anni.anno
        ORDER BY anni.anno DESC;
    """
    cursor.execute(query)
    return cursor.fetchall()


#------------------------- forms.py ------------------------
def extract_sum_all_importi_ricavi_of_protocol(id_protocollo):
    cursor = connection.cursor()
    cursor.execute("""SELECT coalesce(sum(r.importo),0) as tot
                      FROM Contabilita_ricavo r
                      WHERE r.protocollo_id = :proto_id""", {'proto_id': id_protocollo})
    return cursor.fetchone()[0]

def extract_sum_importi_ricavi_of_protocol_excluding_specific_ricavo(id_protocollo, id_ricavo):
    cursor = connection.cursor()
    cursor.execute("""SELECT coalesce(sum(r.importo),0) as tot
                      FROM Contabilita_ricavo r
                      WHERE r.protocollo_id = :proto_id  AND r.id != :ricavo_id""",
                   {'proto_id': id_protocollo, 'ricavo_id': id_ricavo})
    return cursor.fetchone()[0]