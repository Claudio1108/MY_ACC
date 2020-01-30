from django.db import connection

# ------------------------- views.py ------------------------
def calculate_saldo(type_saldo):
    cursor = connection.cursor()
    cursor.execute(
        """  SELECT coalesce(sum(t1.saldo),0)
                        FROM(
                        SELECT importo as saldo
                        FROM Contabilita_ricavo
                        WHERE destinazione = :provenienza
                        UNION
                        SELECT -importo as saldo
                        FROM Contabilita_spesagestione
                        WHERE provenienza = :provenienza
                        UNION
                        SELECT -importo as saldo
                        FROM Contabilita_spesacommessa
                        WHERE provenienza = :provenienza
                        UNION
                        SELECT -importo as saldo
                        FROM Contabilita_guadagnoeffettivo
                        WHERE provenienza = :provenienza) t1""",
        {"provenienza": type_saldo},
    )
    return cursor.fetchone()[0]


def resoconto_spese_gestione(year):
    cursor = connection.cursor()
    query = """ select '01/GENNAIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_spesagestione t1  
                where strftime('%m', t1.data_registrazione) = '01' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                UNION
                select '02/FEBBRAIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_spesagestione t1  
                where strftime('%m', t1.data_registrazione) = '02' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                UNION
                select '03/MARZO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_spesagestione t1  
                where strftime('%m', t1.data_registrazione) = '03' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                UNION
                select '04/APRILE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_spesagestione t1  
                where strftime('%m', t1.data_registrazione) = '04' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                UNION
                select '05/MAGGIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_spesagestione t1  
                where strftime('%m', t1.data_registrazione) = '05' and strftime('%Y', t1.data_registrazione) = '{d[year]}' 
                UNION
                select '06/GIUGNO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_spesagestione t1  
                where strftime('%m', t1.data_registrazione) = '06' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                UNION
                select '07/LUGLIO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_spesagestione t1  
                where strftime('%m', t1.data_registrazione) = '07' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                UNION
                select '08/AGOSTO' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_spesagestione t1  
                where strftime('%m', t1.data_registrazione) = '08' and strftime('%Y', t1.data_registrazione) = '{d[year]}' 
                UNION
                select '09/SETTEMBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_spesagestione t1  
                where strftime('%m', t1.data_registrazione) = '09' and strftime('%Y', t1.data_registrazione) = '{d[year]}' 
                UNION
                select '10/OTTOBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_spesagestione t1  
                where strftime('%m', t1.data_registrazione) = '10' and strftime('%Y', t1.data_registrazione) = '{d[year]}' 
                UNION
                select '11/NOVEMBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_spesagestione t1  
                where strftime('%m', t1.data_registrazione) = '11' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                UNION
                select '12/DICEMBRE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_spesagestione t1  
                where strftime('%m', t1.data_registrazione) = '12' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                UNION
                select 'TOTALE' as mese, coalesce(sum(t1.importo),0) as SpesediGestione, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                from Contabilita_spesagestione t1
                where strftime('%Y', t1.data_registrazione) = '{d[year]}'
                ORDER BY mese ASC;""".format(
        d={"year": str(year)}
    )
    cursor.execute(query)
    return cursor.fetchall()


def resoconto_ricavi(year):
    cursor = connection.cursor()
    query = """ select '01/GENNAIO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico
                    from Contabilita_ricavo t1  
                    where strftime('%m', t1.data_registrazione) = '01' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                    union
                    select '02/FEBBRAIO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1  
                    where strftime('%m', t1.data_registrazione) = '02' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                    union
                    select '03/MARZO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1  
                    where strftime('%m', t1.data_registrazione) = '03' and strftime('%Y', t1.data_registrazione) = '{d[year]}' 
                    union
                    select '04/APRILE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where strftime('%m', t1.data_registrazione) = '04' and strftime('%Y', t1.data_registrazione) = '{d[year]}' 
                    union
                    select '05/MAGGIO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where strftime('%m', t1.data_registrazione) = '05' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                    union
                    select '06/GIUGNO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where strftime('%m', t1.data_registrazione) = '06' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                    union
                    select '07/LUGLIO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where strftime('%m', t1.data_registrazione) = '07' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                    union
                    select '08/AGOSTO' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where strftime('%m', t1.data_registrazione) = '08' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                    union
                    select '09/SETTEMBRE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where strftime('%m', t1.data_registrazione) = '09' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                    union
                    select '10/OTTOBRE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where strftime('%m', t1.data_registrazione) = '10' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                    union
                    select '11/NOVEMBRE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where strftime('%m', t1.data_registrazione) = '11' and strftime('%Y', t1.data_registrazione) = '{d[year]}' 
                    union
                    select '12/DICEMBRE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where strftime('%m', t1.data_registrazione) = '12' and strftime('%Y', t1.data_registrazione) = '{d[year]}' 
                    union
                    select 'TOTALE' as mese, coalesce(sum(t1.importo),0) as ricavo, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico  
                    from Contabilita_ricavo t1
                    where strftime('%Y', t1.data_registrazione) = '{d[year]}'
                    ORDER BY mese ASC;""".format(
        d={"year": str(year)}
    )
    cursor.execute(query)
    return cursor.fetchall()


def resoconto_guadagni_effettivi(year):
    cursor = connection.cursor()
    query = """ select '01/GENNAIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '01' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                           (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '01' and strftime('%Y', t1.data_registrazione) = '{d[year]}') as GuadagniTeorici,
                                           coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                           (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '01' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                           (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '01' and strftime('%Y', t1.data_registrazione) = '{d[year]}')-coalesce(sum(t1.importo),0) as DIfferenza
                   from Contabilita_guadagnoeffettivo t1
                   where strftime('%m', t1.data_registrazione) = '01' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                   union
                   select '02/FEBBRAIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '02' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '02' and strftime('%Y', t1.data_registrazione) = '{d[year]}') as GuadagniTeorici,
                                          coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                          (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '02' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '02' and strftime('%Y', t1.data_registrazione) = '{d[year]}')-coalesce(sum(t1.importo),0) as DIfferenza
                   from Contabilita_guadagnoeffettivo t1
                   where strftime('%m', t1.data_registrazione) = '02' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                   union
                   select '03/MARZO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '03' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '03' and strftime('%Y', t1.data_registrazione) = '{d[year]}') as GuadagniTeorici,
                                          coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                          (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '03' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '03' and strftime('%Y', t1.data_registrazione) = '{d[year]}')-coalesce(sum(t1.importo),0) as DIfferenza
                   from Contabilita_guadagnoeffettivo t1
                   where strftime('%m', t1.data_registrazione) = '03' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                   union
                   select '04/APRILE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '04' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '04' and strftime('%Y', t1.data_registrazione) = '{d[year]}') as GuadagniTeorici,
                                          coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                          (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '04' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '04' and strftime('%Y', t1.data_registrazione) = '{d[year]}')-coalesce(sum(t1.importo),0) as DIfferenza
                   from Contabilita_guadagnoeffettivo t1
                   where strftime('%m', t1.data_registrazione) = '04' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                   union
                   select '05/MAGGIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '05' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '05' and strftime('%Y', t1.data_registrazione) = '{d[year]}') as GuadagniTeorici,
                                          coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                          (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '05' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '05' and strftime('%Y', t1.data_registrazione) = '{d[year]}')-coalesce(sum(t1.importo),0) as DIfferenza
                   from Contabilita_guadagnoeffettivo t1
                   where strftime('%m', t1.data_registrazione) = '05' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                   union
                   select '06/GIUGNO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '06' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '06' and strftime('%Y', t1.data_registrazione) = '{d[year]}') as GuadagniTeorici,
                                          coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                          (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '06' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '06' and strftime('%Y', t1.data_registrazione) = '{d[year]}')-coalesce(sum(t1.importo),0) as DIfferenza
                   from Contabilita_guadagnoeffettivo t1
                   where strftime('%m', t1.data_registrazione) = '06' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                   union
                   select '07/LUGLIO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '07' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '07' and strftime('%Y', t1.data_registrazione) = '{d[year]}') as GuadagniTeorici,
                                          coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                          (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '07' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '07' and strftime('%Y', t1.data_registrazione) = '{d[year]}')-coalesce(sum(t1.importo),0) as DIfferenza
                   from Contabilita_guadagnoeffettivo t1
                   where strftime('%m', t1.data_registrazione) = '07' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                   union
                   select '08/AGOSTO' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '08' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '08' and strftime('%Y', t1.data_registrazione) = '{d[year]}') as GuadagniTeorici,
                                          coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                          (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '08' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '08' and strftime('%Y', t1.data_registrazione) = '{d[year]}')-coalesce(sum(t1.importo),0) as DIfferenza
                   from Contabilita_guadagnoeffettivo t1
                   where strftime('%m', t1.data_registrazione) = '08' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                   union
                   select '09/SETTEMBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '09' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '09' and strftime('%Y', t1.data_registrazione) = '{d[year]}') as GuadagniTeorici,
                                          coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                          (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '09' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '09' and strftime('%Y', t1.data_registrazione) = '{d[year]}')-coalesce(sum(t1.importo),0) as DIfferenza
                   from Contabilita_guadagnoeffettivo t1
                   where strftime('%m', t1.data_registrazione) = '09' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                   union
                   select '10/OTTOBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '10' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '10' and strftime('%Y', t1.data_registrazione) = '{d[year]}') as GuadagniTeorici,
                                          coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                          (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '10' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '10' and strftime('%Y', t1.data_registrazione) = '{d[year]}')-coalesce(sum(t1.importo),0) as DIfferenza
                   from Contabilita_guadagnoeffettivo t1
                   where strftime('%m', t1.data_registrazione) = '10' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                   union
                   select '11/NOVEMBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '11' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '11' and strftime('%Y', t1.data_registrazione) = '{d[year]}') as GuadagniTeorici,
                                          coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                          (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '11' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '11' and strftime('%Y', t1.data_registrazione) = '{d[year]}')-coalesce(sum(t1.importo),0) as DIfferenza
                   from Contabilita_guadagnoeffettivo t1
                   where strftime('%m', t1.data_registrazione) = '11' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                   union
                   select '12/DICEMBRE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '12' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '12' and strftime('%Y', t1.data_registrazione) = '{d[year]}') as GuadagniTeorici,
                                          coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                          (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%m', t1.data_registrazione) = '12' and strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%m', t1.data_registrazione) = '12' and strftime('%Y', t1.data_registrazione) = '{d[year]}')-coalesce(sum(t1.importo),0) as DIfferenza
                   from Contabilita_guadagnoeffettivo t1
                   where strftime('%m', t1.data_registrazione) = '12' and strftime('%Y', t1.data_registrazione) = '{d[year]}'
                   union
                   select 'TOTALE' as mese, (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%Y', t1.data_registrazione) = '{d[year]}') as GuadagniTeorici,
                                          coalesce(sum(t1.importo),0) as GuadagniEffettivi, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Daniele'),2) as Daniele , round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Laura'),2) as Laura, round(coalesce(sum(t1.importo),0) * (select t2.percentuale from Contabilita_socio t2 where t2.nome='Federico'),2) as Federico,
                                          (select coalesce(sum(t2.importo),0) from Contabilita_ricavo t2 where strftime('%Y', t1.data_registrazione) = '{d[year]}') -
                                          (select coalesce(sum(t1.importo),0) from Contabilita_spesagestione t1 where strftime('%Y', t1.data_registrazione) = '{d[year]}')-coalesce(sum(t1.importo),0) as DIfferenza
                   from Contabilita_guadagnoeffettivo t1
                   where strftime('%Y', t1.data_registrazione) = '{d[year]}'	  
                   ORDER BY mese ASC;""".format(
        d={"year": str(year)}
    )
    cursor.execute(query)
    return cursor.fetchall()


def resoconto_contabilita_protocolli():
    cursor = connection.cursor()
    cursor.execute(
        """ SELECT t1.identificativo, t4.nominativo as cliente, t1.referente_id, t1.indirizzo,t1.pratica,t1.parcella,(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id) as entrate,
                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as uscite,
                            t1.parcella-(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id)+
                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as saldo
                       FROM   Contabilita_protocollo t1, Contabilita_rubricaclienti t4
                       WHERE saldo != 0 and t1.cliente_id = t4.id and t1.referente_id is NULL
                       union
                       SELECT t1.identificativo, t4.nominativo as cliente, t5.nominativo, t1.indirizzo,t1.pratica,t1.parcella,(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id) as entrate,
                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as uscite,
                            t1.parcella-(SELECT coalesce(sum(t2.importo), 0) FROM Contabilita_ricavo t2 WHERE t1.id = t2.protocollo_id)+
                            (SELECT coalesce(sum(t3.importo), 0) FROM Contabilita_spesacommessa t3 WHERE t1.id=t3.protocollo_id) as saldo
                       FROM   Contabilita_protocollo t1, Contabilita_rubricaclienti t4, Contabilita_rubricareferenti t5
                       WHERE saldo != 0 and t1.cliente_id = t4.id and t1.referente_id = t5.id
                       ORDER BY t1.identificativo DESC"""
    )
    return cursor.fetchall()


# ------------------------- forms.py ------------------------
def extract_sum_all_importi_ricavi_of_protocol(id_protocollo):
    cursor = connection.cursor()
    cursor.execute(
        """SELECT coalesce(sum(r.importo),0) as tot
                      FROM Contabilita_ricavo r
                      WHERE r.protocollo_id = :proto_id""",
        {"proto_id": id_protocollo},
    )
    return cursor.fetchone()[0]


def extract_sum_importi_ricavi_of_protocol_excluding_specific_ricavo(id_protocollo, id_ricavo):
    cursor = connection.cursor()
    cursor.execute(
        """SELECT coalesce(sum(r.importo),0) as tot
                      FROM Contabilita_ricavo r
                      WHERE r.protocollo_id = :proto_id  AND r.id != :ricavo_id""",
        {"proto_id": id_protocollo, "ricavo_id": id_ricavo},
    )
    return cursor.fetchone()[0]
