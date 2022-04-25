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
    '/Users/sabinal/Desktop/MASTER 2022/DATA/Python kode/ferdigbehandletinput.xls')
pasient_df = pasient_df.reset_index()
diagnose_df = pd.read_excel(
    '/Users/sabinal/Desktop/MASTER 2022/DATA/Python kode/test55.xls')

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
    neste_år = []
    tid_til_overs = []
    tid_tid = []

    stue_ort_1 = Stue('N-01')  # Her har jeg gitt de navn fordi jeg trodde jeg trengte det, men trengte det egentlig ikke , men ikke fjern kan være nyttig
    stue_ort_2 = Stue('N-02')
    stue_ort_3 = Stue('N-03')
    stue_ort_4 = Stue('N-04')

    stue_andre_1 = Stue('N-05')
    stue_andre_2 = Stue('N-06')
    stue_andre_3 = Stue('N-07')
    stue_andre_4 = Stue('N-10')
    stue_andre_5 = Stue('N-12')

    for m in range(1, 13):  # Her går vi gjennom de 12 måneddedne

        skift_stuer = 0

        for t in range(4):  # Her går vi gjennom 7 ukedager, men fordi jeg er dum er index her 0 til 6, å jeg gidder ikke fikse på den <3

            stue_ort_1.reset_stue()  # Her har jeg gitt de navn fordi jeg trodde jeg trengte det, men trengte det egentlig ikke , men ikke fjern kan være nyttig
            stue_ort_2.reset_stue()
            stue_ort_3.reset_stue()
            stue_ort_4.reset_stue()

            stue_andre_1.reset_stue()
            stue_andre_2.reset_stue()
            stue_andre_3.reset_stue()
            stue_andre_4.reset_stue()
            stue_andre_5.reset_stue()

            skift_stuer += 1

            for j in range(7):
                skift = 0  # Teller skift
                dag = []
                tidligkveld = []
                kveld = []
                natt = []
                test = []

                for i in pasient_liste:  # Sorterer de inn i de ulike skiftene for å bli letter eå jobbe med
                    if i.month == m:
                        if i.ukedag == j:
                            if i.behandlet == False:
                                if i.tid == 1:
                                    dag.append(i)
                                elif i.tid == 2:
                                    tidligkveld.append(i)
                                elif i.tid == 3:
                                    kveld.append(i)
                                elif i.tid == 4:
                                    natt.append(i)

                for k in [dag, tidligkveld, kveld,
                          natt]:  # Her velger vi så kalrt hvilket skift i jobber med

                    k.extend(neste_skift)
                    neste_skift = []
                    skift += 1
                    total_tid_o = stue_ort_1.fast_tid(skift)
                    total_tid_a = stue_andre_1.fast_tid(skift)

                    # Det som kommer under her er den beste implementeringen av hvordan man sakl ta med elektiv tid. Jeg bare utførte den før man gjorde noe annet. Kan hende at vi burde kjøre røde pasienter først, sånn egentlig, men det vil gjøre koden saktere
                    for index, row in elektiv.iterrows():
                        if row['Måned'] == m and row['Ukedag'] == j and row[
                            'TidsIntervallStue'] == skift:
                            if row['Stue'] == 'N-01':
                                stue_ort_1.update(skift, (row['StueTidMin'])/4)
                            elif row['Stue'] == 'N-02':
                                stue_ort_2.update(skift, (row['StueTidMin'])/4)
                            elif row['Stue'] == 'N-03':
                                stue_ort_3.update(skift, (row['StueTidMin'])/4)
                            elif row['Stue'] == 'N-04':
                                stue_ort_4.update(skift, (row['StueTidMin'])/4)
                            elif row['Stue'] == 'N-05':
                                stue_andre_1.update(skift, (row['StueTidMin'])/4)
                            elif row['Stue'] == 'N-06':
                                stue_andre_2.update(skift, (row['StueTidMin'])/4)
                            elif row['Stue'] == 'N-07':
                                stue_andre_3.update(skift, (row['StueTidMin'])/4)
                            elif row['Stue'] == 'N-10':
                                stue_andre_4.update(skift, (row['StueTidMin'])/4)
                            elif row['Stue'] == 'N-12':
                                stue_andre_5.update(skift, (row['StueTidMin'])/4)

                    if skift == 1 and skift_stuer <= 1:
                        liste_stuer_o = [stue_ort_1, stue_ort_2, stue_ort_3, stue_ort_4]
                        liste_stuer_a = [stue_andre_1, stue_andre_2, stue_andre_3, stue_andre_4,
                                         stue_andre_5]

                        liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)
                        liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)

                        stuer_skift_1_o = liste_stuer_o
                        stuer_skift_1_a = liste_stuer_a


                    elif skift == 2 and skift_stuer <= 1:

                        liste_stuer_o = [stue_ort_1, stue_ort_2, stue_ort_3, stue_ort_4]
                        liste_stuer_a = [stue_andre_1, stue_andre_2, stue_andre_3, stue_andre_4,
                                         stue_andre_5]

                        liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)
                        liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)

                        liste_stuer_o = liste_stuer_o[0:4]
                        liste_stuer_a = liste_stuer_a[0:5]

                        stuer_skift_2_o = liste_stuer_o
                        stuer_skift_2_a = liste_stuer_a

                    elif skift == 3 and skift_stuer <= 1:
                        liste_stuer_o = [stue_ort_1, stue_ort_2, stue_ort_3, stue_ort_4]
                        liste_stuer_a = [stue_andre_1, stue_andre_2, stue_andre_3, stue_andre_4,
                                         stue_andre_5]

                        liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)
                        liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)

                        liste_stuer_o = liste_stuer_o[0:2]
                        liste_stuer_a = liste_stuer_a[0:4]

                        stuer_skift_3_o = liste_stuer_o
                        stuer_skift_3_a = liste_stuer_a

                    elif skift == 4 and skift_stuer <= 1:
                        liste_stuer_o = [stue_ort_1, stue_ort_2, stue_ort_3, stue_ort_4]
                        liste_stuer_a = [stue_andre_1, stue_andre_2, stue_andre_3, stue_andre_4,
                                         stue_andre_5]

                        liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)
                        liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)

                        liste_stuer_o = liste_stuer_o[0:1]
                        liste_stuer_a = liste_stuer_a[0:1]

                        stuer_skift_4_o = liste_stuer_o
                        stuer_skift_4_a = liste_stuer_a

                    elif skift == 1 and skift_stuer > 1:
                        liste_stuer_o = stuer_skift_1_o
                        liste_stuer_a = stuer_skift_1_a

                        liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)
                        liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)

                    elif skift == 2 and skift_stuer <= 1:

                        liste_stuer_o = stuer_skift_2_o
                        liste_stuer_a = stuer_skift_2_a

                        liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)
                        liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)

                        liste_stuer_o = liste_stuer_o[0:4]
                        liste_stuer_a = liste_stuer_a[0:5]

                    elif skift == 3 and skift_stuer <= 1:
                        liste_stuer_o = stuer_skift_3_o
                        liste_stuer_a = stuer_skift_3_a

                        liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)
                        liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)

                        liste_stuer_o = liste_stuer_o[0:2]
                        liste_stuer_a = liste_stuer_a[0:4]

                    elif skift == 4 and skift_stuer <= 1:
                        liste_stuer_o = stuer_skift_4_o
                        liste_stuer_a = stuer_skift_4_a

                        liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)
                        liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)

                        liste_stuer_o = liste_stuer_o[0:1]
                        liste_stuer_a = liste_stuer_a[0:1]

                    for i in k:  # Her fikser vi litt tid å sånn, føler denne forkalrer seg selv ?
                        if i.fagOmrade == 'Ortopedi' and i.hast == 'Red':
                            if liste_stuer_o[0].get_time(skift) - i.stuetid - 45 >= 0:
                                i.inntid = liste_stuer_o[0].get_time(skift)
                                liste_stuer_o[0].update(skift, i.stuetid)
                                ferdig_pasienter.append(i)
                                i.behandlet = True
                                i.ventetid += stue_ort_1.fast_tid(skift) - i.inntid
                                liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)

                            else:
                                neste_skift.append(i)
                                i.ventetid += stue_ort_1.fast_tid_delt(skift)
                                i.tid += 1
                                if i.tid == 4 and i.ukedag < 6:
                                    i.ukedag += 1
                                    i.tid = 1
                                elif i.tid == 4 and i.ukedag == 6:
                                    i.ukedag = 0
                                    i.tid = 1
                                if t == 4:
                                    i.month += 1
                                if i.month == 13:
                                    i.month = 1
                                    neste_år.append(i)

                        elif not i.fagOmrade == 'Ortopedi' and i.hast == 'Red':
                            if liste_stuer_a[0].get_time(skift) - i.stuetid - 45 >= 0:
                                i.inntid = liste_stuer_a[0].get_time(skift)
                                liste_stuer_a[0].update(skift, i.stuetid)
                                ferdig_pasienter.append(i)
                                i.behandlet = True
                                i.ventetid += stue_andre_1.fast_tid(skift) - i.inntid
                                liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)

                            else:
                                neste_skift.append(i)
                                i.ventetid += stue_andre_1.fast_tid_delt(skift)
                                i.tid += 1
                                if i.tid == 4 and i.ukedag < 6:
                                    i.ukedag += 1
                                    i.tid = 1
                                elif i.tid == 4 and i.ukedag == 6:
                                    i.ukedag = 0
                                    i.tid = 1
                                if t == 4:
                                    i.month += 1
                                if i.month == 13:
                                    i.month = 1
                                    neste_år.append(i)

                        elif i.fagOmrade == 'Ortopedi' and i.hast == 'Yellow' and skift != 4:
                            if liste_stuer_o[0].get_time(skift) - i.stuetid - 45 >= 0:
                                i.inntid = liste_stuer_o[0].get_time(skift)
                                liste_stuer_o[0].update(skift, i.stuetid)
                                ferdig_pasienter.append(i)
                                i.behandlet = True
                                i.ventetid += stue_ort_1.fast_tid(skift) - i.inntid
                                liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)
                            else:
                                neste_skift.append(i)
                                i.ventetid += stue_ort_1.fast_tid_delt(skift)
                                i.tid += 1
                                if i.tid == 4 and i.ukedag < 6:
                                    i.ukedag += 1
                                    i.tid = 1
                                elif i.tid == 4 and i.ukedag == 6:
                                    i.ukedag = 0
                                    i.tid = 1
                                if t == 4:
                                    i.month += 1
                                if i.month == 13:
                                    i.month = 1
                                    neste_år.append(i)

                        elif i.fagOmrade == 'Ortopedi' and i.hast == 'Yellow' and skift == 4:

                            i.ventetid += stue_ort_1.fast_tid_delt(skift)

                            if i.tid == 4 and i.ukedag < 6:
                                i.ukedag += 1
                                i.tid = 1
                            elif i.tid == 4 and i.ukedag == 6:
                                i.ukedag = 0
                                i.tid = 1
                            if t == 4:
                                i.month += 1
                            if i.month == 13:
                                i.month = 1
                                neste_år.append(i)


                        elif not i.fagOmrade == 'Ortopedi' and i.hast == 'Yellow' and skift != 4:
                            if liste_stuer_a[0].get_time(skift) - i.stuetid - 45 >= 0:
                                i.inntid = liste_stuer_a[0].get_time(skift)
                                liste_stuer_a[0].update(skift, i.stuetid)
                                ferdig_pasienter.append(i)
                                i.behandlet = True
                                i.ventetid += stue_andre_1.fast_tid(skift) - i.inntid
                                liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)
                            else:
                                neste_skift.append(i)
                                i.ventetid += stue_andre_1.fast_tid_delt(skift)
                                i.tid += 1
                                if i.tid == 4 and i.ukedag < 6:
                                    i.ukedag += 1
                                    i.tid = 1
                                elif i.tid == 4 and i.ukedag == 6:
                                    i.ukedag = 0
                                    i.tid = 1
                                if t == 4:
                                    i.month += 1
                                if i.month == 13:
                                    i.month = 1
                                    neste_år.append(i)

                        elif not i.fagOmrade == 'Ortopedi' and i.hast == 'Yellow' and skift == 4:

                            i.ventetid += stue_ort_1.fast_tid_delt(skift)

                            if i.tid == 4 and i.ukedag < 6:
                                i.ukedag += 1
                                i.tid = 1
                            elif i.tid == 4 and i.ukedag == 6:
                                i.ukedag = 0
                                i.tid = 1
                            if t == 4:
                                i.month += 1
                            if i.month == 13:
                                i.month = 1
                                neste_år.append(i)

                        elif i.fagOmrade == 'Ortopedi' and i.hast == 'Green' and skift != 4:
                            if liste_stuer_o[0].get_time(skift) - i.stuetid - 45 >= 0:
                                i.inntid = liste_stuer_o[0].get_time(skift)
                                liste_stuer_o[0].update(skift, i.stuetid)
                                ferdig_pasienter.append(i)
                                i.behandlet = True
                                i.ventetid += stue_ort_1.fast_tid(skift) - i.inntid
                                liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)
                            else:
                                neste_skift.append(i)
                                i.ventetid += stue_ort_1.fast_tid_delt(skift)
                                i.tid += 1
                                if i.tid == 4 and i.ukedag < 6:
                                    i.ukedag += 1
                                    i.tid = 1
                                elif i.tid == 4 and i.ukedag == 6:
                                    i.ukedag = 0
                                    i.tid = 1
                                if t == 4:
                                    i.month += 1
                                if i.month == 13:
                                    i.month = 1
                                    neste_år.append(i)

                        elif i.fagOmrade == 'Ortopedi' and i.hast == 'Green' and skift == 4:

                            i.ventetid += stue_ort_1.fast_tid_delt(skift)

                            if i.tid == 4 and i.ukedag < 6:
                                i.ukedag += 1
                                i.tid = 1
                            elif i.tid == 4 and i.ukedag == 6:
                                i.ukedag = 0
                                i.tid = 1
                            if t == 4:
                                i.month += 1
                            if i.month == 13:
                                i.month = 1
                                neste_år.append(i)

                        elif not i.fagOmrade == 'Ortopedi' and i.hast == 'Green' and skift != 4:
                            if liste_stuer_a[0].get_time(skift) - i.stuetid - 45 >= 0:
                                i.inntid = liste_stuer_a[0].get_time(skift)
                                liste_stuer_a[0].update(skift, i.stuetid)
                                ferdig_pasienter.append(i)
                                i.behandlet = True
                                i.ventetid += stue_andre_1.fast_tid(skift) - i.inntid
                                liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)
                            else:
                                neste_skift.append(i)
                                i.ventetid += stue_andre_1.fast_tid_delt(skift)
                                i.tid += 1
                                if i.tid == 4 and i.ukedag < 6:
                                    i.ukedag += 1
                                    i.tid = 1
                                elif i.tid == 4 and i.ukedag == 6:
                                    i.ukedag = 0
                                    i.tid = 1
                                if t == 4:
                                    i.month += 1
                                if i.month == 13:
                                    i.month = 1
                                    neste_år.append(i)

                        elif not i.fagOmrade == 'Ortopedi' and i.hast == 'Green' and skift == 4:

                            i.ventetid += stue_ort_1.fast_tid_delt(skift)

                            if i.tid == 4 and i.ukedag < 6:
                                i.ukedag += 1
                                i.tid = 1
                            elif i.tid == 4 and i.ukedag == 6:
                                i.ukedag = 0
                                i.tid = 1
                            if t == 4:
                                i.month += 1
                            if i.month == 13:
                                i.month = 1
                                neste_år.append(i)

                neste_skift = []

    df = pd.DataFrame([vars(f) for f in
                       ferdig_pasienter])  # Henter ut verdier fordi lister er dumme og df er best <3
    df_2 = pd.DataFrame([vars(f) for f in neste_år])
    df_3 = pd.DataFrame([vars(f) for f in pasient_liste])
    df_4 = pd.DataFrame([vars(f) for f in tid_til_overs])
    df.to_excel("ferdigbehandletoutput.xls")
    df_2.to_excel("nesteår.xls")
    df_3.to_excel('bugs.xls')
    df_4.to_excel('tid til overs.xls')

    # Det er masse piss her, men tror disse kommentarene skal gjøre det lettere å forstå. Jeg er veldi lei denne koden atm.
    # Vil egentlig bare kaste den ut vinduet <3 <3
