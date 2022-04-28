# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'

import pandas as pd

from Simuleringsmodell.oppsettpasienter import TrafikkLys
from Simuleringsmodell.trafikklys import Stue

if __name__ == '__main__':
    df = pd.read_excel("C:/Users/Eier/Documents/Master 2022/data/DATA JOBBE MED/NBH SOP MED KODER 2019.xlsx")
    diagnose_df = pd.read_excel('C:/Users/Eier/Documents/Master 2022/diagnoser.xlsx')
    df = df.reset_index()
    sim = TrafikkLys()
    sim.initer_pasienter(pasient_df=df)
    stue = Stue()
    stue.fordel_trafikklys(sim.pasient_liste, diagnose_df)
    for _ in range (10):
        print(sim.pasient_liste[_].trafikklys)
    #print(df)


