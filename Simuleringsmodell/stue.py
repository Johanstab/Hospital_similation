# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'

import pandas as pd

from trafikklys import Red, Yellow, Green


class Sykehus:

    parametere = {}

    @classmethod
    def sett_parametere(cls, nye_parametere):
        for parameter in nye_parametere:
            if parameter not in cls.parametere:
                raise KeyError('Parameteren eksisterer ikke:' + nye_parametere[0])

    def __init__(self):
        self.stuer = []

    def fordel_trafikklys(self, pasient_liste, Diagnose_df):

        for pasient in pasient_liste:
            for index, row in Diagnose_df.iterrows():
                if pasient.diagnose == row['DiagnoseGruppe'] and row['Hastegrad'] == 'Rød':
                    pasient.hast= 'Red'
                    break
                elif pasient.diagnose == row['DiagnoseGruppe'] and row['Hastegrad'] == 'Gul':
                    pasient.hast = 'Yellow'
                    break
                elif pasient.diagnose == row['DiagnoseGruppe'] and row['Hastegrad'] == 'Grønn':
                    pasient.hast = 'Green'
                    break
                else:
                    continue

    def fikser_dager(self, pasient_liste):

        for pasient in pasient_liste:
            if pasient.tid == 'Dag':
                pasient.tid = 1
            elif pasient.tid == 'Tidlig Kveld':
                pasient.tid = 2
            elif pasient.tid == 'Kveld':
                pasient.tid = 3
            elif pasient.tid == 'Natt':
                pasient.tid = 4

    def kalk_elektiv(self, df):

        elektiv = df[df['ErØhjelp'] != 'ø-hjelp']
        ufiltrert_tid = elektiv[['Måned', 'Ukedag', 'TidsIntervallStue', 'StueTidMin']]
        #filtrert_tid = ufiltrert_tid[ufiltrert_tid['Stue'].str.contains('N-08|N-09|N-11|N-14|N-15') == False]

        elektiv_tid = ufiltrert_tid.groupby(['Måned', 'Ukedag', 'TidsIntervallStue'])['StueTidMin'].sum()
        antall_elektiv = ufiltrert_tid.groupby(['Måned', 'Ukedag', 'TidsIntervallStue'])['StueTidMin'].count()

        df_to_use = elektiv_tid.to_frame().join(antall_elektiv, lsuffix='_caller', rsuffix='_other')

        return elektiv_tid, df_to_use



class OrtoStue(Sykehus):
    parametere = {'Dag': 4,
                  'Tidlig kveld': 3,
                  'Kveld': 2}

    fagomrade = ['Ortopedi']

    def __init__(self):
        super().__init__()


class RestStue(Sykehus):

    parametere = {'Dag': 5,
                  'Tidlig kveld': 4,
                  'Kveld': 3}

    fagomrade = ['Gynekologi', 'Gastrokirurgi']

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    stue = Sykehus()
    stue1 = RestStue()
    elektiv_df = stue.kalk_elektiv(pd.read_excel('/Users/sabinal/Desktop/MASTER 2022/DATA/Python '
                                                 'kode/Data NBH SOP 2019 Koder & Trafikklys '
                                                 '1.xls')) # Må legge til filepath

    print(elektiv_df[1])




