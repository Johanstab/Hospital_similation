# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'

import pandas as pd


class Stue:

    def __init__(self, fag, hoytid=False):

        self.hoytid = hoytid
        self.fag = fag

        if not hoytid:
            self.skift_1 = 4320 * self.fag.parametere['Dag'] * 4
            self.skift_2 = 1050 * self.fag.parametere['Tidlig kveld'] * 4
            self.skift_3 = 1350 * self.fag.parametere['Kveld'] * 4
            self.skift_4 = 480 * 4


        else:
            self.skift_1 = 4000
            self.skift_2 = 800
            self.skift_3 = 1000
            self.skift_4 = 400

    def get_time(self, skift):

        if skift == 1:
            return self.skift_1
        elif skift == 2:
            return self.skift_2
        elif skift == 3:
            return self.skift_3
        elif skift == 4:
            return self.skift_4

    def fast_tid(self, skift):

        if skift == 1:
            return 4320 * self.fag.parametere['Dag'] * 4
        elif skift == 2:
            return 1050 * self.fag.parametere['Tidlig kveld'] * 4
        elif skift == 3:
            return 1350 * self.fag.parametere['Kveld'] * 4
        elif skift == 4:
            return 480 * 4


if __name__ == '__main__':
    import pandas as pd
    from sykehus import Sykehus
    from stue import Stue
    from trafikklys import TrafikkLys

    sim = TrafikkLys()
    stue = Sykehus()
    pasient_liste = []
    pasient_df = pd.read_excel(
        '/Users/sabinal/Desktop/MASTER 2022/DATA/Python kode/Test.xls')
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

    sim.initer_pasienter(pasient_df)
    pasient_liste = sim.pasient_liste
    stue.fordel_trafikklys(pasient_liste, diagnose_df)
    stue.fikser_dager(pasient_liste)  # Viktig å fikse sånn at string blir til tall
    ferdig_pasienter = []
    neste_skift = []

    skift = 0
    dag = []
    tidligkveld = []
    kveld = []
    natt = []
    test = []

    for i in pasient_liste:  # Sorterer de inn i de ulike skiftene for å bli letter eå jobbe med
        if i.tid == 1:
            dag.append(i)
        elif i.tid == 2:
            tidligkveld.append(i)
        elif i.tid == 3:
            kveld.append(i)
        elif i.tid == 4:
            natt.append(i)

    for i in kveld:
        i.ukedag = 5

    df = pd.DataFrame([vars(f) for f in pasient_liste]) #Henter ut verdier fordi lister er dumme og df er best <3
    df.to_excel("output35.xls")
