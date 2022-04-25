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
    '/Users/sabinal/Desktop/MASTER 2022/DATA/Python kode/Test.xls')
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

    for m in range(1, 13):

        for j in range(7):

            stue_ort_1 = Stue()
            stue_ort_2 = Stue()
            stue_ort_3 = Stue()
            stue_ort_4 = Stue()

            stue_andre_1 = Stue()
            stue_andre_2 = Stue()
            stue_andre_3 = Stue()
            stue_andre_4 = Stue()
            stue_andre_5 = Stue()

            liste_stuer_o = [stue_ort_1, stue_ort_2, stue_ort_3, stue_ort_4]
            liste_stuer_a = [stue_andre_1, stue_andre_2, stue_andre_3, stue_andre_4, stue_andre_5]

            t = 0
            q = 0
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

            dag.sort(key=lambda x: x.ventetid, reverse=True)
            tidligkveld.sort(key=lambda x: x.ventetid, reverse=True)
            kveld.sort(key=lambda x: x.ventetid, reverse=True)
            natt.sort(key=lambda x: x.ventetid, reverse=True)

            for k in [dag, tidligkveld, kveld, natt]:

                k.extend(neste_skift)
                neste_skift = []
                skift += 1
                tid_o_liste = []
                total_tid_o_liste = []
                tid_a_liste = []
                total_tid_a_liste = []

                for i in liste_stuer_o:
                    tid_o_liste.append(i.get_time(skift))
                    total_tid_o_liste.append(i.fast_tid(skift))

                for i in liste_stuer_a:
                    tid_a_liste.append(i.get_time(skift))
                    total_tid_a_liste.append(i.fast_tid(skift))

                for i in k:
                    if i.fagOmrade == 'Ortopedi' and i.hast == 'Red':
                            if max(tid_o_liste) - i.stuetid - 45 >= 0:
                                i.inntid = max(tid_o_liste)
                                tid_o_liste[j] = i.inntid - i.stuetid - 45
                                ferdig_pasienter.append(i)
                                i.ventetid += total_tid_o_liste[j] - i.inntid + i.stuetid
                            else:
                                neste_skift.append(i)
                                if k == natt and i.ukedag < 6:
                                    i.ukedag += 1
                                elif k == natt and i.ukedag == 6:
                                    i.ukedag = 0

                    elif not i.fagOmrade == 'Ortopedi' and i.hast == 'Red':
                        for j in range(len(tid_a_liste)):
                            if tid_a_liste[j] - i.stuetid - 45 >= 0:
                                i.inntid = tid_a_liste[j]
                                tid_a_liste[j] = tid_a_liste[j] - i.stuetid - 45
                                ferdig_pasienter.append(i)
                                i.ventetid += total_tid_a_liste[j] - i.inntid + i.stuetid
                                break
                            else:
                                neste_skift.append(i)
                                if k == natt and i.ukedag < 6:
                                    i.ukedag += 1
                                elif k == natt and i.ukedag == 6:
                                    i.ukedag = 0

                for index, row in elektiv.iterrows():
                    if row['Måned'] == m and row['Ukedag'] == j and row[
                        'TidsIntervallStue'] == skift:
                        if row['Fagområde'] == 'Ortopedi':
                            for i in tid_o_liste:
                                i = i - row['StueTidMin'] / (len(tid_o_liste)) - (
                                        45 / len(tid_o_liste))
                        else:
                            for j in tid_a_liste:
                                j = j - row['StueTidMin'] / (len(tid_a_liste)) - (
                                        45 / len(tid_a_liste))

                for i in k:
                    if i.fagOmrade == 'Ortopedi' and i.hast == 'Yellow':
                        for j in range(len(tid_o_liste)):
                            if tid_o_liste[j] - i.stuetid - 45 >= 0:
                                i.inntid = tid_o_liste[j]
                                tid_o_liste[j] = tid_o_liste[j] - i.stuetid - 45
                                ferdig_pasienter.append(i)
                                i.ventetid += total_tid_o_liste[j] - i.inntid + i.stuetid
                                break
                            else:
                                neste_skift.append(i)
                                if k == natt and i.ukedag < 6:
                                    i.ukedag += 1
                                elif k == natt and i.ukedag == 6:
                                    i.ukedag = 0

                    elif not i.fagOmrade == 'Ortopedi' and i.hast == 'Yellow':
                        for j in range(len(tid_a_liste)):
                            if tid_a_liste[j] - i.stuetid - 45 >= 0:
                                i.inntid = tid_a_liste[j]
                                tid_a_liste[j] = tid_a_liste[j] - i.stuetid - 45
                                ferdig_pasienter.append(i)
                                i.ventetid += total_tid_a_liste[j] - i.inntid + i.stuetid
                                break
                            else:
                                neste_skift.append(i)
                                if k == natt and i.ukedag < 6:
                                    i.ukedag += 1
                                elif k == natt and i.ukedag == 6:
                                    i.ukedag = 0
                for i in k:
                    if i.fagOmrade == 'Ortopedi' and i.hast == 'Green':
                        for j in range(len(tid_o_liste)):
                            if tid_o_liste[j] - i.stuetid - 45 >= 0:
                                i.inntid = tid_o_liste[j]
                                tid_o_liste[j] = tid_o_liste[j] - i.stuetid - 45
                                ferdig_pasienter.append(i)
                                i.ventetid += total_tid_o_liste[j] - i.inntid + i.stuetid
                                break
                            else:
                                neste_skift.append(i)
                                if k == natt and i.ukedag < 6:
                                    i.ukedag += 1
                                elif k == natt and i.ukedag == 6:
                                    i.ukedag = 0

                    elif not i.fagOmrade == 'Ortopedi' and i.hast == 'Green':
                        for j in range(len(tid_a_liste)):
                            if tid_a_liste[j] - i.stuetid - 45 >= 0:
                                i.inntid = tid_a_liste[j]
                                tid_a_liste[j] = tid_a_liste[j] - i.stuetid - 45
                                ferdig_pasienter.append(i)
                                i.ventetid += total_tid_a_liste[j] - i.inntid + i.stuetid
                                break
                            else:
                                neste_skift.append(i)
                                if k == natt and i.ukedag < 6:
                                    i.ukedag += 1
                                elif k == natt and i.ukedag == 6:
                                    i.ukedag = 0

            for i in neste_skift:
                i.month += 1

    for i in ferdig_pasienter:
        print(i.pasientNr)

    df = pd.DataFrame([vars(f) for f in ferdig_pasienter])
    df_2 = pd.DataFrame([vars(f) for f in neste_skift])
    df.to_excel("output1.xls")
    df_2.to_excel("output2.xls")
