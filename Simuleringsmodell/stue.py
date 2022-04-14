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

        """Funksjonen konverterer dataframen som kommer in til en ny dataframe som har filtrert ut
        den elektive

        :param df:
        :return df_to_use: Ny df med mengde tid brukt i måneden per ukedag + skift + stue
        """

        # elektiv = df[df['ErØhjelp'] != 'ø-hjelp']
        elektiv = df
        elektiv.loc[elektiv['ErØhjelp'] == 'ø-hjelp', 'StueTidMin'] = None
        ufiltrert_tid = elektiv[['Måned', 'Ukedag', 'TidsIntervallStue', 'StueTidMin', 'Stue']]
        filtrert_tid = ufiltrert_tid[ufiltrert_tid['Stue'].str.contains('N-08|N-09|N-11|N-14|N-15') == False]

        elektiv_tid = filtrert_tid.groupby(['Måned', 'Ukedag', 'TidsIntervallStue', 'Stue'],
                                           dropna=False)['StueTidMin'].sum()
        antall_elektiv = filtrert_tid.groupby(['Måned', 'Ukedag', 'TidsIntervallStue', 'Stue'],
                                              dropna=False)['StueTidMin'].count()
        # tid_ohjelp = filtrert_tid.groupby(['Måned', 'Ukedag', 'TidsIntervallStue'])['StueTidMin'].sum()

        df_to_use = elektiv_tid.to_frame().join(antall_elektiv, lsuffix='_caller', rsuffix='_other')

        return df_to_use

    def lag_fordelingsstruktur(self):

        pass


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
    org_df = pd.read_excel('C:/Users/Eier/Documents/Master 2022/data/DATA JOBBE MED/NBH SOP MED KODER 2019.xlsx')
    elektiv_df, df, ohjelp = stue.kalk_elektiv(org_df) # Må legge til filepath
