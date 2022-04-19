# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'


class Sykehus:

    def __init__(self):
        pass

    def fordel_trafikklys(self, pasient_liste, Diagnose_df):

        for pasient in pasient_liste:
            for index, row in Diagnose_df.iterrows():
                if pasient.diagnose == row['DiagnoseGruppe'] and row['Hastegrad'] == 'Rød':
                    pasient.hast = 'Red'
                    pasient.hast_nummer = 3 # Denne la jeg til for å sortere lettere :)
                    break
                elif pasient.diagnose == row['DiagnoseGruppe'] and row['Hastegrad'] == 'Gul':
                    pasient.hast = 'Yellow'
                    pasient.hast_nummer = 2
                    break
                elif pasient.diagnose == row['DiagnoseGruppe'] and row['Hastegrad'] == 'Grønn':
                    pasient.hast = 'Green'
                    pasient.hast_nummer = 1
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
