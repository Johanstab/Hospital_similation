# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'

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
