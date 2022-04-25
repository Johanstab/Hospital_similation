# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'

import pandas as pd
from pasient import Pasient
from trafikklys import TrafikkLys
from sykehus import Sykehus, OrtoStue, RestStue
from stue import Stue

sim = TrafikkLys()
stue = Sykehus()
orto = OrtoStue()
andre = RestStue()
pasient_liste = []
pasient_df = pd.read_excel(
    '/Users/sabinal/Desktop/MASTER 2022/DATA/Python kode/output.xls')
pasient_df = pasient_df.reset_index()
diagnose_df = pd.read_excel(
    '/Users/sabinal/Desktop/MASTER 2022/DATA/Python kode/test3.xls')

df = pd.read_excel(
    '/Users/sabinal/Desktop/MASTER 2022/DATA/Python kode/Data NBH SOP 2019 Koder & Trafikklys 1.xls')

elektiv = pd.read_excel('/Users/sabinal/Desktop/MASTER 2022/DATA/Python kode/test4.xls')
elektiv = elektiv.replace(to_replace=["Dag", "Tidligkveld", "Kveld", "Natt"],
                          value=[int(1), int(2), int(3), int(4)])
elektiv = elektiv.replace(to_replace=["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag",
                                      "Lørdag", "Søndag"], value=[0, 1, 2, 3, 4, 5, 6])

if __name__ == '__main__':

    sim.initer_pasienter(pasient_df)
    pasient_liste = sim.pasient_liste
    stue.fordel_trafikklys(pasient_liste, diagnose_df)
    stue.fikser_dager(pasient_liste)
    jan_liste = []
    ferdig_pasienter = []
    neste_skift = []
    liste_stuer_o = []
    liste_stuer_a = []

    for m in range(1, 13):

        for j in range(7):

            stue_ort_1 = Stue('N-01')
            stue_ort_2 = Stue('N-02')
            stue_ort_3 = Stue('N-03')
            stue_ort_4 = Stue('N-04')

            stue_andre_1 = Stue('N-05')
            stue_andre_2 = Stue('N-06')
            stue_andre_3 = Stue('N-07')
            stue_andre_4 = Stue('N-10')
            stue_andre_5 = Stue('N-12')

            skift = 0
            dag = []
            tidligkveld = []
            kveld = []
            natt = []
            test = []

            for i in pasient_liste:
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

            for k in [dag, tidligkveld, kveld, natt]:

                k.extend(neste_skift)
                neste_skift = []
                skift += 1
                total_tid_o = stue_ort_1.fast_tid(skift)
                total_tid_a = stue_andre_1.fast_tid(skift)

                for index, row in elektiv.iterrows():
                    if row['Måned'] == m and row['Ukedag'] == j and row[
                        'TidsIntervallStue'] == skift:
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

                if skift == 1:
                    liste_stuer_o = [stue_ort_1.get_time(skift), stue_ort_2.get_time(skift),
                                     stue_ort_3.get_time(skift), stue_ort_4.get_time(skift)]
                    liste_stuer_a = [stue_andre_1.get_time(skift), stue_andre_2.get_time(skift),
                                     stue_andre_3.get_time(skift), stue_andre_4.get_time(skift),
                                     stue_andre_5.get_time(skift)]

                    tid_o = max(liste_stuer_o)
                    tid_o_index = liste_stuer_o.index(tid_o)

                    tid_a = max(liste_stuer_a)
                    tid_a_index = liste_stuer_a.index(tid_a)

                elif skift == 2:
                    liste_stuer_o = [stue_ort_1.get_time(skift), stue_ort_2.get_time(skift),
                                     stue_ort_3.get_time(skift)]

                    liste_stuer_a = [stue_andre_1.get_time(skift), stue_andre_2.get_time(skift),
                                     stue_andre_3.get_time(skift), stue_andre_4.get_time(skift)]



                    tid_o = max(liste_stuer_o)
                    tid_o_index = liste_stuer_o.index(tid_o)

                    tid_a = max(liste_stuer_a)
                    tid_a_index = liste_stuer_a.index(tid_a)

                elif skift == 3:
                    liste_stuer_o = [stue_ort_1.get_time(skift), stue_ort_2.get_time(skift)]

                    liste_stuer_a = [stue_andre_1.get_time(skift), stue_andre_2.get_time(skift),
                                     stue_andre_3.get_time(skift)]

                    tid_o = max(liste_stuer_o)
                    tid_o_index = liste_stuer_o.index(tid_o)

                    tid_a = max(liste_stuer_a)
                    tid_a_index = liste_stuer_a.index(tid_a)

                elif skift == 4:
                    liste_stuer_o = [stue_ort_1.get_time(skift)]

                    liste_stuer_a = [stue_andre_1.get_time(skift)]

                    tid_o = max(liste_stuer_o)
                    tid_o_index = liste_stuer_o.index(tid_o)

                    tid_a = max(liste_stuer_a)
                    tid_a_index = liste_stuer_a.index(tid_a)

                for i in k:

                    if i.fagOmrade == 'Ortopedi' and i.hast == 'Red':
                        if liste_stuer_o[tid_o_index] - i.stuetid - 45 >= 0:
                            i.inntid = liste_stuer_o[tid_o_index]
                            liste_stuer_o[tid_o_index] += - i.stuetid - 45
                            ferdig_pasienter.append(i)
                            i.ventetid += stue_ort_1.fast_tid(skift) - i.inntid + i.stuetid

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
                            i.ventetid += stue_andre_1.fast_tid(skift) - i.inntid + i.stuetid

                        else:
                            neste_skift.append(i)
                            if k == natt and i.ukedag < 6:
                                i.ukedag += 1
                            elif k == natt and i.ukedag == 6:
                                i.ukedag = 0

                    elif i.fagOmrade == 'Ortopedi' and i.hast == 'Yellow':
                        if liste_stuer_o[tid_o_index] - i.stuetid - 45 >= 0:
                            i.inntid = liste_stuer_o[tid_o_index]
                            liste_stuer_o[tid_o_index] += - i.stuetid - 45
                            ferdig_pasienter.append(i)
                            i.ventetid += stue_ort_1.fast_tid(skift) - i.inntid + i.stuetid
                        else:
                            neste_skift.append(i)
                            i.ventetid += stue_ort_1.fast_tid(skift)
                            if i.ventetid > 1440:
                                i.hast_nummer = 1
                            if k == natt and i.ukedag < 6:
                                i.ukedag += 1
                            elif k == natt and i.ukedag == 6:
                                i.ukedag = 0

                    elif not i.fagOmrade == 'Ortopedi' and i.hast == 'Yellow':
                        if liste_stuer_a[tid_a_index] - i.stuetid - 45 >= 0:
                            i.inntid = liste_stuer_a[tid_a_index]
                            liste_stuer_a[tid_a_index] += - i.stuetid - 45
                            ferdig_pasienter.append(i)
                            i.ventetid += stue_andre_1.fast_tid(skift) - i.inntid + i.stuetid
                        else:
                            neste_skift.append(i)
                            i.ventetid += stue_andre_1.fast_tid(skift)
                            if i.ventetid > 1440:
                                i.hast_nummer = 1
                            if k == natt and i.ukedag < 6:
                                i.ukedag += 1
                            elif k == natt and i.ukedag == 6:
                                i.ukedag = 0

                    elif i.fagOmrade == 'Ortopedi' and i.hast == 'Green':
                        if liste_stuer_o[tid_o_index] - i.stuetid - 45 >= 0:
                            i.inntid = liste_stuer_o[tid_o_index]
                            liste_stuer_o[tid_o_index] += - i.stuetid - 45
                            ferdig_pasienter.append(i)
                            i.ventetid += stue_ort_1.fast_tid(skift) - i.inntid + i.stuetid
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
                            i.ventetid += stue_andre_1.fast_tid(skift) - i.inntid + i.stuetid
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

    df = pd.DataFrame([vars(f) for f in ferdig_pasienter])
    df_2 = pd.DataFrame([vars(f) for f in neste_skift])
    df.to_excel("output3.xls")
    df_2.to_excel("output4.xls")
