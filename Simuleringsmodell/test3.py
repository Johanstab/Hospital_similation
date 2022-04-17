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
    '/Users/sabinal/Desktop/MASTER 2022/DATA/Python kode/test.xls')
pasient_df = pasient_df.reset_index()
diagnose_df = pd.read_excel(
    '/Users/sabinal/Desktop/MASTER 2022/DATA/Python kode/test2.xls')

df = pd.read_excel(
    '/Users/sabinal/Desktop/MASTER 2022/DATA/Python kode/Data NBH SOP 2019 '
    'Koder & Trafikklys 1.xls')

if __name__ == '__main__':

    #tid = 10000

    #elektiv = pd.read_excel('/Users/sabinal/Desktop/MASTER 2022/DATA/Python kode/test4.xls')

    #elektiv = elektiv.replace(to_replace=["Dag", "Tidligkveld", "Kveld", "Natt"],
               #value=[int(1),int(2),int(3),int(4)])

    #print(elektiv)

    #for index, row in elektiv.iterrows():
        #if row['Måned'] == 1 and row['Ukedag'] == 'Søndag' and row['TidsIntervallStue'] == 4:
            #tid = tid - row['StueTidMin']


    #print(tid)

