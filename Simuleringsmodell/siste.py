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
elektiv = pd.read_excel(
    '/Users/sabinal/Desktop/untitled folder 2/Elektiv tid brukt.xls')
elektiv = elektiv.replace(to_replace=["Dag", "Tidligkveld", "Kveld", "Natt"],
                          value=[int(1), int(2), int(3), int(4)])
elektiv = elektiv.replace(to_replace=["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag",
                                      "Lørdag", "Søndag"], value=[0, 1, 2, 3, 4, 5, 6])

if __name__ == '__main__':

    sim.initer_pasienter(pasient_df)
    pasient_liste = sim.pasient_liste
    stue.fordel_trafikklys(pasient_liste, diagnose_df)
    stue.fikser_dager(pasient_liste)
    ferdig_pasienter = []
    neste_skift = []
    liste_stuer_o = []
    liste_stuer_a = []
    neste_year = []


    # Setter opp stuene for første gang:
    stue_ort_1 = Stue('N-01')
    stue_ort_2 = Stue('N-02')
    stue_ort_3 = Stue('N-03')
    stue_ort_4 = Stue('N-04')

    stue_andre_1 = Stue('N-05')
    stue_andre_2 = Stue('N-06')
    stue_andre_3 = Stue('N-07')
    stue_andre_4 = Stue('N-10')
    stue_andre_5 = Stue('N-12')

    for month in range(1, 13):

        for week in range(1, 5):

            for day in range(7):
                # Resetter stuene slik at man får "ny" tid hver uke

                stue_ort_1.reset_stue()
                stue_ort_2.reset_stue()
                stue_ort_3.reset_stue()
                stue_ort_4.reset_stue()

                stue_andre_1.reset_stue()
                stue_andre_2.reset_stue()
                stue_andre_3.reset_stue()
                stue_andre_4.reset_stue()
                stue_andre_5.reset_stue()

                skift = 0
                dag = []
                tidligkveld = []
                kveld = []
                natt = []
                neste_skift = []

                for pasient in pasient_liste:

                    if pasient.month == month:

                        if pasient.ukedag == day:

                            if not pasient.behandlet:

                                if pasient.tid == 1:
                                    dag.append(pasient)

                                elif pasient.tid == 2:
                                    tidligkveld.append(pasient)

                                elif pasient.tid == 3:
                                    kveld.append(pasient)

                                elif pasient.tid == 4:
                                    natt.append(pasient)

                for skift_tid in [dag, tidligkveld, kveld, natt]:

                    skift += 1

                    skift_tid.extend(neste_skift)

                    skift_tid.sort(key=lambda x: (x.hast_nummer, x.ventetid), reverse=True)

                    neste_skift = []

                    for index, row in elektiv.iterrows():
                        if row['Måned'] == month and row['Ukedag'] == day and row[
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

                    if skift == 1:
                        liste_stuer_o = [stue_ort_1, stue_ort_2, stue_ort_3, stue_ort_4]
                        liste_stuer_a = [stue_andre_1, stue_andre_2, stue_andre_3, stue_andre_4,
                                         stue_andre_5]

                        liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)
                        liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)


                    elif skift == 2:

                        liste_stuer_o = [stue_ort_1, stue_ort_2, stue_ort_3, stue_ort_4]
                        liste_stuer_a = [stue_andre_1, stue_andre_2, stue_andre_3, stue_andre_4,
                                         stue_andre_5]

                        liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)
                        liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)

                        liste_stuer_o = liste_stuer_o[0:4]
                        liste_stuer_a = liste_stuer_a[0:5]


                    elif skift == 3:
                        liste_stuer_o = [stue_ort_1, stue_ort_2, stue_ort_3, stue_ort_4]
                        liste_stuer_a = [stue_andre_1, stue_andre_2, stue_andre_3, stue_andre_4,
                                         stue_andre_5]

                        liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)
                        liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)

                        liste_stuer_o = liste_stuer_o[0:2]
                        liste_stuer_a = liste_stuer_a[0:4]


                    elif skift == 4:
                        liste_stuer_o = [stue_ort_1, stue_ort_2, stue_ort_3, stue_ort_4]
                        liste_stuer_a = [stue_andre_1, stue_andre_2, stue_andre_3, stue_andre_4,
                                         stue_andre_5]

                        liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)
                        liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)

                        liste_stuer_o = liste_stuer_o[0:1]
                        liste_stuer_a = liste_stuer_a[0:1]



                    for person in skift_tid:
                        if person.fagOmrade == 'Ortopedi' and person.hast == 'Red':
                            if liste_stuer_o[0].get_time(skift) - person.stuetid - 45 >= 0:
                                person.inntid = liste_stuer_o[0].get_time(skift)
                                liste_stuer_o[0].update(skift, person.stuetid)
                                ferdig_pasienter.append(person)
                                person.behandlet = True
                                person.ventetid += stue_ort_1.fast_tid(skift) - person.inntid
                                liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)

                            else:
                                person.ventetid += stue_ort_1.fast_tid_delt(skift)
                                neste_skift.append(person)

                                if person.tid < 4:

                                    person.tid += 1

                                else:

                                    person.tid = 1

                                    if person.ukedag < 6:

                                        person.ukedag += 1

                                    else:

                                        person.ukedag = 0

                                        if week >= 4:

                                            person.month += 1

                                            if person.month > 12:
                                                person.month = 1
                                                neste_year.append(person)

                        if not person.fagOmrade == 'Ortopedi' and person.hast == 'Red':
                            if liste_stuer_a[0].get_time(skift) - person.stuetid - 45 >= 0:
                                person.inntid = liste_stuer_a[0].get_time(skift)
                                liste_stuer_a[0].update(skift, person.stuetid)
                                ferdig_pasienter.append(person)
                                person.behandlet = True
                                person.ventetid += stue_andre_1.fast_tid(skift) - person.inntid
                                liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)

                            else:
                                person.ventetid += stue_ort_1.fast_tid_delt(skift)
                                neste_skift.append(person)

                                if person.tid < 4:

                                    person.tid += 1

                                else:

                                    person.tid = 1

                                    if person.ukedag < 6:

                                        person.ukedag += 1

                                    else:

                                        person.ukedag = 0

                                        if week >= 4:
                                            person.month += 1

                                            if person.month > 12:
                                                person.month = 1
                                                neste_year.append(person)

                        if person.fagOmrade == 'Ortopedi' and person.hast == 'Yellow' and skift != 4:
                            if liste_stuer_o[0].get_time(skift) - person.stuetid - 45 >= 0:
                                person.inntid = liste_stuer_o[0].get_time(skift)
                                liste_stuer_o[0].update(skift, person.stuetid)
                                ferdig_pasienter.append(person)
                                person.behandlet = True
                                person.ventetid += stue_ort_1.fast_tid(skift) - person.inntid
                                liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)

                            else:
                                person.ventetid += stue_ort_1.fast_tid_delt(skift)
                                neste_skift.append(person)

                                if person.tid < 4:

                                    person.tid += 1

                                else:

                                    person.tid = 1

                                    if person.ukedag < 6:

                                        person.ukedag += 1

                                    else:

                                        person.ukedag = 0

                                        if week >= 4:
                                            person.month += 1

                                            if person.month > 12:
                                                person.month = 1
                                                neste_year.append(person)

                        if not person.fagOmrade == 'Ortopedi' and person.hast == 'Yellow' and skift != 4:
                            if liste_stuer_a[0].get_time(skift) - person.stuetid - 45 >= 0:
                                person.inntid = liste_stuer_a[0].get_time(skift)
                                liste_stuer_a[0].update(skift, person.stuetid)
                                ferdig_pasienter.append(person)
                                person.behandlet = True
                                person.ventetid += stue_andre_1.fast_tid(skift) - person.inntid
                                liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)

                            else:
                                person.ventetid += stue_ort_1.fast_tid_delt(skift)
                                neste_skift.append(person)

                                if person.tid < 4:

                                    person.tid += 1

                                else:

                                    person.tid = 1

                                    if person.ukedag < 6:

                                        person.ukedag += 1

                                    else:

                                        person.ukedag = 0

                                        if week >= 4:
                                            person.month += 1

                                            if person.month > 12:
                                                person.month = 1
                                                neste_year.append(person)



                        elif person.fagOmrade == 'Ortopedi' and person.hast == 'Yellow' and skift == 4:

                            person.ventetid += stue_ort_1.fast_tid_delt(skift)

                            if person.tid < 4:

                                person.tid += 1

                            else:

                                person.tid = 1

                                if person.ukedag < 6:

                                    person.ukedag += 1

                                else:

                                    person.ukedag = 0

                                    if week >= 4:
                                        person.month += 1

                                        if person.month > 12:
                                            person.month = 1
                                            neste_year.append(person)


                        elif not person.fagOmrade == 'Ortopedi' and person.hast == 'Yellow' and skift == 4:

                            person.ventetid += stue_andre_1.fast_tid_delt(skift)

                            if person.tid < 4:

                                person.tid += 1

                            else:

                                person.tid = 1

                                if person.ukedag < 6:

                                    person.ukedag += 1

                                else:

                                    person.ukedag = 0

                                    if week >= 4:
                                        person.month += 1

                                        if person.month > 12:
                                            person.month = 1
                                            neste_year.append(person)

                        if person.fagOmrade == 'Ortopedi' and person.hast == 'Green' and skift != 4:
                            if liste_stuer_o[0].get_time(skift) - person.stuetid - 45 >= 0:
                                person.inntid = liste_stuer_o[0].get_time(skift)
                                liste_stuer_o[0].update(skift, person.stuetid)
                                ferdig_pasienter.append(person)
                                person.behandlet = True
                                person.ventetid += stue_ort_1.fast_tid(skift) - person.inntid
                                liste_stuer_o.sort(key=lambda x: x.get_time(skift), reverse=True)

                            else:
                                person.ventetid += stue_ort_1.fast_tid_delt(skift)
                                neste_skift.append(person)

                                if person.tid < 4:

                                    person.tid += 1

                                else:

                                    person.tid = 1

                                    if person.ukedag < 6:

                                        person.ukedag += 1

                                    else:

                                        person.ukedag = 0

                                        if week >= 4:
                                            person.month += 1

                                            if person.month > 12:
                                                person.month = 1
                                                neste_year.append(person)

                        if not person.fagOmrade == 'Ortopedi' and person.hast == 'Green' and skift != 4:
                            if liste_stuer_a[0].get_time(skift) - person.stuetid - 45 >= 0:
                                person.inntid = liste_stuer_a[0].get_time(skift)
                                liste_stuer_a[0].update(skift, person.stuetid)
                                ferdig_pasienter.append(person)
                                person.behandlet = True
                                person.ventetid += stue_andre_1.fast_tid(skift) - person.inntid
                                liste_stuer_a.sort(key=lambda x: x.get_time(skift), reverse=True)

                            else:
                                person.ventetid += stue_ort_1.fast_tid_delt(skift)
                                neste_skift.append(person)

                                if person.tid < 4:

                                    person.tid += 1

                                else:

                                    person.tid = 1

                                    if person.ukedag < 6:

                                        person.ukedag += 1

                                    else:

                                        person.ukedag = 0

                                        if week >= 4:
                                            person.month += 1

                                            if person.month > 12:
                                                person.month = 1
                                                neste_year.append(person)

                        elif person.fagOmrade == 'Ortopedi' and person.hast == 'Green' and skift == 4:

                            person.ventetid += stue_ort_1.fast_tid_delt(skift)

                            if person.tid < 4:

                                person.tid += 1

                            else:

                                person.tid = 1

                                if person.ukedag < 6:

                                    person.ukedag += 1

                                else:

                                    person.ukedag = 0

                                    if week >= 4:
                                        person.month += 1

                                        if person.month > 12:
                                            person.month = 1
                                            neste_year.append(person)

                        elif not person.fagOmrade == 'Ortopedi' and person.hast == 'Green' and skift == 4:

                            person.ventetid += stue_andre_1.fast_tid_delt(skift)

                            if person.tid < 4:

                                person.tid += 1

                            else:

                                person.tid = 1

                                if person.ukedag < 6:

                                    person.ukedag += 1

                                else:

                                    person.ukedag = 0

                                    if week >= 4:
                                        person.month += 1

                                        if person.month > 12:
                                            person.month = 1
                                            neste_year.append(person)

    df = pd.DataFrame([vars(f) for f in ferdig_pasienter])
    df_2 = pd.DataFrame([vars(f) for f in neste_year])
    df_3 = pd.DataFrame([vars(f) for f in pasient_liste])

    df.to_excel("ferdigbehandletoutput ny.xls")
    df_2.to_excel("nesteår ny.xls")
    df_3.to_excel('pasienter ny.xls')


