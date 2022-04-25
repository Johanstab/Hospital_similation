# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'

from pasient import Pasient


class TrafikkLys:
    """Superklasse for trafikklysene"""

    parametere = {}

    @classmethod
    def sett_parametere(cls, nye_parametere):

        for parameter in nye_parametere:
            if parameter not in cls.parametere:
                raise KeyError('Paramteren eksisterer ikke: ' + nye_parametere[0])

        cls.parametere.update(nye_parametere)

    def __init__(self):

        self.pasient_liste = []

    def initer_pasienter(self, pasient_df):

        for index, row in pasient_df.iterrows():
            self.pasient_liste.append(Pasient(row['PasNr'], row['DiagnoseGruppe'],
                                              row['Fagområde'], row['OprType'],
                                              row['Måned'], row['AnnkomstDag'],
                                              row['AnnkomstTidspunkt'], row['StueTidMin'],
                                              row['ErØhjelp']))