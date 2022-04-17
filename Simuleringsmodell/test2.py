# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'

import pandas as pd
from pasient import Pasient
from trafikklys import TrafikkLys
from stue import Sykehus, OrtoStue, RestStue
from test import Stue

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
                                      "Lørdag","Søndag"], value=[0,1, 2, 3, 4, 5, 6])

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

            stue_ort = Stue(orto)
            stue_andre = Stue(andre)
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
                tid_o = stue_ort.get_time(skift)
                total_tid_o = stue_ort.fast_tid(skift)
                tid_a = stue_andre.get_time(skift)
                total_tid_a = stue_andre.fast_tid(skift)
                antall_o = 0
                antall_a = 0

                for i in k:
                    if i.fagOmrade == 'Ortopedi' and i.hast == 'Red':
                        if tid_o - i.stuetid - 45 >= 0:
                            i.inntid = tid_o
                            tid_o = tid_o - i.stuetid - 45
                            ferdig_pasienter.append(i)
                            if antall_o < 4:
                                i.ventetid += i.stuetid
                                antall_o += 1
                            elif antall_o == 4:
                                i.ventetid += total_tid_o - i.inntid + i.stuetid
                                antall_o +=0
                        else:
                            neste_skift.append(i)
                            if k == natt and i.ukedag < 6:
                                i.ukedag += 1
                            elif k == natt and i.ukedag == 6:
                                i.ukedag = 0

                    elif not i.fagOmrade == 'Ortopedi' and i.hast == 'Red':
                        if tid_a  - i.stuetid - 45 >= 0:
                            i.inntid = tid_a
                            tid_a  = tid_a  - i.stuetid - 45
                            ferdig_pasienter.append(i)
                            if antall_a < 5:
                                i.ventetid += i.stuetid
                                antall_a += 1
                            elif antall_a == 5:
                                i.ventetid += total_tid_a - i.inntid + i.stuetid
                                antall_a += 0
                        else:
                            neste_skift.append(i)
                            if k == natt and i.ukedag < 6:
                                i.ukedag += 1
                            elif k == natt and i.ukedag == 6:
                                i.ukedag = 0

                for index, row in elektiv.iterrows():
                    if row['Måned'] == m and row['Ukedag'] == j and row['TidsIntervallStue'] == skift:
                        if row['Fagområde'] == 'Ortopedi':
                            tid_o = tid_o - row['StueTidMin'] - 45
                        else:
                            tid_a = tid_a - row['StueTidMin'] - 45

                for i in k:
                    if i.fagOmrade == 'Ortopedi' and i.hast == 'Yellow':
                        if tid_o - i.stuetid - 45 >= 0:
                            i.inntid = tid_o
                            tid_o = tid_o - i.stuetid - 45
                            ferdig_pasienter.append(i)
                            i.ventetid += total_tid_o - i.inntid + i.stuetid
                        else:
                            neste_skift.append(i)
                            i.ventetid += stue_ort.get_time(skift)

                            if k == natt and i.ukedag < 6:
                                i.ukedag += 1
                            elif k == natt and i.ukedag == 6:
                                i.ukedag = 0

                    elif not i.fagOmrade == 'Ortopedi' and i.hast == 'Yellow':
                        if tid_a - i.stuetid - 45 >= 0:
                            i.inntid = tid_a
                            tid_a = tid_a - i.stuetid - 45
                            ferdig_pasienter.append(i)
                            i.ventetid += total_tid_a - i.inntid + i.stuetid
                        else:
                            neste_skift.append(i)
                            i.ventetid += stue_ort.get_time(skift)

                            if k == natt and i.ukedag < 6:
                                i.ukedag += 1
                            elif k == natt and i.ukedag == 6:
                                i.ukedag = 0

                for i in k:
                    if i.fagOmrade == 'Ortopedi' and i.hast == 'Green':
                        if tid_o - i.stuetid - 45 >= 0:
                            i.inntid = tid_o
                            tid_o = tid_o - i.stuetid - 45
                            ferdig_pasienter.append(i)
                            i.ventetid += total_tid_o - i.inntid + i.stuetid
                        else:
                            neste_skift.append(i)
                            i.ventetid += stue_ort.get_time(skift)

                            if k == natt and i.ukedag < 6:
                                i.ukedag += 1
                            elif k == natt and i.ukedag == 6:
                                i.ukedag = 0

                    elif not i.fagOmrade == 'Ortopedi' and i.hast == 'Green':
                        if tid_a - i.stuetid - 45 >= 0:
                            i.inntid = tid_a
                            tid_a = tid_a - i.stuetid - 45
                            ferdig_pasienter.append(i)
                            i.ventetid += total_tid_a - i.inntid + i.stuetid
                        else:
                            neste_skift.append(i)
                            i.ventetid += stue_ort.get_time(skift)

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
