# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'

import pandas as pd
from sykehus import Sykehus
from stue import Stue
from trafikklys import TrafikkLys

sim = TrafikkLys()
stue = Sykehus()
pasient_liste = []
pasient_df = pd.read_excel(
    '/Users/sabinal/Desktop/MASTER 2022/DATA/Python kode/output.xls')
pasient_df = pasient_df.reset_index()
diagnose_df = pd.read_excel(
    '/Users/sabinal/Desktop/MASTER 2022/DATA/Python kode/test3.xls')

df = pd.read_excel(
    '/Users/sabinal/Desktop/MASTER 2022/DATA/Python kode/Data NBH SOP 2019 Koder & Trafikklys 1.xls')

elektiv = pd.read_excel(
    '/Users/sabinal/Desktop/MASTER 2022/DATA/Python kode/test4.xls')  # Dette er en fil jeg lagde i R studio. fordi det å jobbe med tupels var helt jævlig <3 Dette kan kanskje bli en funksjon
elektiv = elektiv.replace(to_replace=["Dag", "Tidligkveld", "Kveld", "Natt"],
                          value=[int(1), int(2), int(3), int(4)])
elektiv = elektiv.replace(to_replace=["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag",
                                      "Lørdag", "Søndag"], value=[0, 1, 2, 3, 4, 5, 6])

if __name__ == '__main__':

    sim.initer_pasienter(pasient_df)
    pasient_liste = sim.pasient_liste
    stue.fordel_trafikklys(pasient_liste, diagnose_df)
    stue.fikser_dager(pasient_liste)  # Viktig å fikse sånn at string blir til tall
    ferdig_pasienter = []
    neste_skift = []
    liste_stuer_o = []
    liste_stuer_a = []

    for m in range(1, 13):  # Her går vi gjennom de 12 måneddedne

        for j in range(
                7):  # Her går vi gjennom 7 ukedager, men fordi jeg er dum er index her 0 til 6, å jeg gidder ikke fikse på den <3

            stue_ort_1 = Stue(
                'N-01')  # Her har jeg gitt de navn fordi jeg trodde jeg trengte det, men trengte det egentlig ikke , men ikke fjern kan være nyttig
            stue_ort_2 = Stue('N-02')
            stue_ort_3 = Stue('N-03')
            stue_ort_4 = Stue('N-04')

            stue_andre_1 = Stue('N-05')
            stue_andre_2 = Stue('N-06')
            stue_andre_3 = Stue('N-07')
            stue_andre_4 = Stue('N-10')
            stue_andre_5 = Stue('N-12')

            skift = 0  # Teller skift
            dag = []
            tidligkveld = []
            kveld = []
            natt = []
            test = []

            for i in pasient_liste:  # Sorterer de inn i de ulike skiftene for å bli letter eå jobbe med
                if i.month == m:
                    if i.ukedag == j:
                        if i.tid == 1:
                            dag.append(i)
                        elif i.tid == 2:
                            tidligkveld.append(i)
                        elif i.tid == 3:
                            kveld.append(i)
                        elif i.tid == 4:
                            natt.append(i)

            dag.sort(key=lambda x: (x.hast_nummer, x.ventetid),
                     reverse=True)  # Her er mitt tapre forsøk på å sorte slik at man både tar hensyn til farge å ventetid. Ikke at det har hjulpet, men hei jeg prøvde
            tidligkveld.sort(key=lambda x: (x.hast_nummer, x.ventetid), reverse=True)
            kveld.sort(key=lambda x: (x.hast_nummer, x.ventetid), reverse=True)
            natt.sort(key=lambda x: (x.hast_nummer, x.ventetid), reverse=True)

            for k in [dag, tidligkveld, kveld,
                      natt]:  # Her velger vi så kalrt hvilket skift i jobber med

                k.extend(neste_skift)
                neste_skift = []
                skift += 1
                total_tid_o = stue_ort_1.fast_tid(skift)
                total_tid_a = stue_andre_1.fast_tid(skift)

                if skift == 1:
                    liste_stuer_o = [stue_ort_1.get_time(skift), stue_ort_2.get_time(skift),
                                     stue_ort_3.get_time(skift), stue_ort_4.get_time(skift)]
                    liste_stuer_a = [stue_andre_1.get_time(skift), stue_andre_2.get_time(skift),
                                     stue_andre_3.get_time(skift), stue_andre_4.get_time(skift),
                                     stue_andre_5.get_time(skift)]

                    tid_o = max(
                        liste_stuer_o)  # Dette er litt komp å forstå, men hør her. Vi finner den stuen som har mest tid(dette blir oppdaert lengre nede). Grunnen til det er fordi det er jo flere stuer som er oprative samtdig, så dette er måten vi tar hensyn til det på.
                    tid_o_index = liste_stuer_o.index(tid_o)

                    tid_a = max(liste_stuer_a)
                    tid_a_index = liste_stuer_a.index(tid_a)

                elif skift == 2:

                    liste_stuer_o = [stue_ort_1.get_time(skift), stue_ort_2.get_time(skift),
                                     stue_ort_3.get_time(skift), stue_ort_4.get_time(skift)]
                    liste_stuer_a = [stue_andre_1.get_time(skift), stue_andre_2.get_time(skift),
                                     stue_andre_3.get_time(skift), stue_andre_4.get_time(skift),
                                     stue_andre_5.get_time(skift)]

                    liste_stuer_o.sort(
                        reverse=True)  # Denne biten er gøy. Siden vi har et redusert antall med stuer, så vil vi jo bruke de stuene som har mest tid igjen. Nå når jeg skriver denne kommentaren innser jeg at det ikke har en dritt å si, fordi stuetiden blir jo satt på ny ved nytt skift <3 nå hater jeg livet hahah
                    liste_stuer_a.sort(reverse=True)

                    liste_stuer_o = liste_stuer_o[0:4]
                    liste_stuer_a = liste_stuer_a[0:5]

                    tid_o = max(liste_stuer_o)
                    tid_o_index = liste_stuer_o.index(tid_o)

                    tid_a = max(liste_stuer_a)
                    tid_a_index = liste_stuer_a.index(tid_a)

                elif skift == 3:
                    liste_stuer_o = [stue_ort_1.get_time(skift), stue_ort_2.get_time(skift),
                                     stue_ort_3.get_time(skift), stue_ort_4.get_time(skift)]
                    liste_stuer_a = [stue_andre_1.get_time(skift), stue_andre_2.get_time(skift),
                                     stue_andre_3.get_time(skift), stue_andre_4.get_time(skift),
                                     stue_andre_5.get_time(skift)]

                    liste_stuer_o.sort(reverse=True)
                    liste_stuer_a.sort(reverse=True)

                    liste_stuer_o = liste_stuer_o[0:2]
                    liste_stuer_a = liste_stuer_a[0:4]

                    tid_o = max(liste_stuer_o)
                    tid_o_index = liste_stuer_o.index(tid_o)

                    tid_a = max(liste_stuer_a)
                    tid_a_index = liste_stuer_a.index(tid_a)

                elif skift == 4:
                    liste_stuer_o = [stue_ort_1.get_time(skift), stue_ort_2.get_time(skift),
                                     stue_ort_3.get_time(skift), stue_ort_4.get_time(skift)]
                    liste_stuer_a = [stue_andre_1.get_time(skift), stue_andre_2.get_time(skift),
                                     stue_andre_3.get_time(skift), stue_andre_4.get_time(skift),
                                     stue_andre_5.get_time(skift)]

                    liste_stuer_o.sort(reverse=True)
                    liste_stuer_a.sort(reverse=True)

                    liste_stuer_o = liste_stuer_o[0:1]
                    liste_stuer_a = liste_stuer_a[0:1]

                    tid_o = max(liste_stuer_o)
                    tid_o_index = liste_stuer_o.index(tid_o)

                    tid_a = max(liste_stuer_a)
                    tid_a_index = liste_stuer_a.index(tid_a)

                for i in k:  # Her fikser vi litt tid å sånn, føler denne forkalrer seg selv ?

                    if i.fagOmrade == 'Ortopedi' and i.hast == 'Red':
                        if liste_stuer_o[tid_o_index] - i.stuetid - 45 >= 0:
                            i.inntid = liste_stuer_o[tid_o_index]
                            liste_stuer_o[tid_o_index] += - i.stuetid - 45
                            ferdig_pasienter.append(i)
                            i.ventetid += stue_ort_1.fast_tid(skift) - i.inntid

                        else:
                            neste_skift.append(i)
                            if k == natt and i.ukedag < 6:
                                i.ukedag += 1
                            elif k == natt and i.ukedag == 6:
                                i.ukedag = 0

                    elif not i.fagOmrade == 'Ortopedi' and i.hast == 'Red':
                        if liste_stuer_a[tid_a_index] - i.stuetid - 45 >= 0:
                            i.inntid = liste_stuer_a[tid_a_index]
                            liste_stuer_a[tid_a_index] += - i.stuetid - 45
                            ferdig_pasienter.append(i)
                            i.ventetid += stue_andre_1.fast_tid(skift) - i.inntid

                        else:
                            neste_skift.append(i)
                            if k == natt and i.ukedag < 6:
                                i.ukedag += 1
                            elif k == natt and i.ukedag == 6:
                                i.ukedag = 0

                # Det som kommer under her er den beste implementeringen av hvordan man sakl ta med elektiv tid. Jeg bare utførte den før man gjorde noe annet. Kan hende at vi burde kjøre røde pasienter først, sånn egentlig, men det vil gjøre koden saktere
                for index, row in elektiv.iterrows():
                    if row['Måned'] == m and row['Ukedag'] == j and row['TidsIntervallStue'] == skift:
                        if row['Stue'] == 'N-01':
                            tid = stue_ort_1.get_time(skift)
                            tid += - row['StueTidMin'] - 45
                        elif row['Stue'] == 'N-02':
                            tid = stue_ort_2.get_time(skift)
                            tid += - row['StueTidMin'] - 45
                        elif row['Stue'] == 'N-03':
                            tid = stue_ort_3.get_time(skift)
                            tid += - row['StueTidMin'] - 45
                        elif row['Stue'] == 'N-04':
                            tid = stue_ort_4.get_time(skift)
                            tid += - row['StueTidMin'] - 45
                        elif row['Stue'] == 'N-05':
                            tid = stue_andre_1.get_time(skift)
                            tid += - row['StueTidMin'] - 45
                        elif row['Stue'] == 'N-06':
                            tid = stue_andre_2.get_time(skift)
                            tid += - row['StueTidMin'] - 45
                        elif row['Stue'] == 'N-07':
                            tid = stue_andre_3.get_time(skift)
                            tid += - row['StueTidMin'] - 45
                        elif row['Stue'] == 'N-10':
                            tid = stue_andre_1.get_time(skift)
                            tid += - row['StueTidMin'] - 45
                        elif row['Stue'] == 'N-12':
                            tid = stue_andre_1.get_time(skift)
                            tid += - row['StueTidMin'] - 45

                for i in k:
                    if i.fagOmrade == 'Ortopedi' and i.hast == 'Yellow':
                        if liste_stuer_o[tid_o_index] - i.stuetid - 45 >= 0:
                            i.inntid = liste_stuer_o[tid_o_index]
                            liste_stuer_o[tid_o_index] += - i.stuetid - 45
                            ferdig_pasienter.append(i)
                            i.ventetid += stue_ort_1.fast_tid(skift) - i.inntid
                        else:
                            neste_skift.append(i)
                            i.ventetid += stue_ort_1.fast_tid(skift)
                            if k == natt and i.ukedag < 6:
                                i.ukedag += 1
                            elif k == natt and i.ukedag == 6:
                                i.ukedag = 0

                    elif not i.fagOmrade == 'Ortopedi' and i.hast == 'Yellow':
                        if liste_stuer_a[tid_a_index] - i.stuetid - 45 >= 0:
                            i.inntid = liste_stuer_a[tid_a_index]
                            liste_stuer_a[tid_a_index] += - i.stuetid - 45
                            ferdig_pasienter.append(i)
                            i.ventetid += stue_andre_1.fast_tid(skift) - i.inntid
                        else:
                            neste_skift.append(i)
                            i.ventetid += stue_andre_1.fast_tid(skift)
                            if k == natt and i.ukedag < 6:
                                i.ukedag += 1
                            elif k == natt and i.ukedag == 6:
                                i.ukedag = 0

                    elif i.fagOmrade == 'Ortopedi' and i.hast == 'Green':
                        if liste_stuer_o[tid_o_index] - i.stuetid - 45 >= 0:
                            i.inntid = liste_stuer_o[tid_o_index]
                            liste_stuer_o[tid_o_index] += - i.stuetid - 45
                            ferdig_pasienter.append(i)
                            i.ventetid += stue_ort_1.fast_tid(skift) - i.inntid
                        else:
                            neste_skift.append(i)
                            i.ventetid += stue_ort_1.fast_tid(skift)

                            if k == natt and i.ukedag < 6:
                                i.ukedag += 1
                            elif k == natt and i.ukedag == 6:
                                i.ukedag = 0

                    elif not i.fagOmrade == 'Ortopedi' and i.hast == 'Green':
                        if liste_stuer_a[tid_a_index] - i.stuetid - 45 >= 0:
                            i.inntid = liste_stuer_a[tid_a_index]
                            liste_stuer_a[tid_a_index] += - i.stuetid - 45
                            ferdig_pasienter.append(i)
                            i.ventetid += stue_andre_1.fast_tid(skift) - i.inntid
                        else:
                            neste_skift.append(i)
                            i.ventetid += stue_andre_1.fast_tid(skift)

                            if k == natt and i.ukedag < 6:
                                i.ukedag += 1
                            elif k == natt and i.ukedag == 6:
                                i.ukedag = 0

                    tid_o = max(liste_stuer_o)
                    tid_o_index = liste_stuer_o.index(tid_o)

                    tid_a = max(liste_stuer_a)
                    tid_a_index = liste_stuer_a.index(tid_a)

            for i in neste_skift:
                i.month += 1

    df = pd.DataFrame([vars(f) for f in
                       ferdig_pasienter])  # Henter ut verdier fordi lister er dumme og df er best <3
    df_2 = pd.DataFrame([vars(f) for f in neste_skift])
    df.to_excel("output3.xls")
    df_2.to_excel("output4.xls")

    # Det er masse piss her, men tror disse kommentarene skal gjøre det lettere å forstå. Jeg er veldi lei denne koden atm.
    # Vil egentlig bare kaste den ut vinduet <3 <3
