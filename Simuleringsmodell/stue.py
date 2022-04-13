# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'

import pandas as pd

from .trafikklys import Red, Yellow, Green


class Stue:

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
                    pasient.trafikklys = Red
                    break
                elif pasient.diagnose == row['DiagnoseGruppe'] and row['Hastegrad'] == 'Gul':
                    pasient.trafikklys = Yellow
                    break
                elif pasient.diagnose == row['DiagnoseGruppe'] and row['Hastegrad'] == 'Grønn':
                    pasient.trafikklys = Green
                    break
                else:
                    continue

    def kalk_elektiv(self, df):

        elektiv = df[df['ErØhjelp'] != 'ø-hjelp']
        ufiltrert_tid = elektiv[['Måned', 'Ukedag', 'TidsIntervallStue', 'StueTidMin', 'Stue']]
        filtrert_tid = ufiltrert_tid[ufiltrert_tid['Stue'].str.contains('N-08|N-09|N-11|N-14|N-15') == False]

        elektiv_tid = filtrert_tid.groupby(['Måned', 'Ukedag', 'TidsIntervallStue', 'Stue'])['StueTidMin'].sum()
        antall_elektiv = filtrert_tid.groupby(['Måned', 'Ukedag', 'TidsIntervallStue', 'Stue'])['StueTidMin'].count()

        df_to_use = elektiv_tid.to_frame().join(antall_elektiv, lsuffix='_caller', rsuffix='_other')

        return elektiv_tid, df_to_use


class OrtoStue(Stue):
    parametere = {'Dag': 4,
                  'Tidlig kveld': 3,
                  'Kveld': 2}

    fagomrade = ['Ortopedi']

    def __init__(self):
        super().__init__()


class RestStue(Stue):

    parametere = {'Dag': 5,
                  'Tidlig kveld': 4,
                  'Kveld': 3}

    fagomrade = ['Gynekologi', 'Gastrokirurgi']

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    stue = Stue()
    elektiv_df = stue.kalk_elektiv(pd.read_excel('RIKTIG FIL')) # Må legge til filepath
