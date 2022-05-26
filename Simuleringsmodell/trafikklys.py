# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'


class Trafikklys:

    def __init__(self):
        pass

    def fordel_trafikklys(self, pasient_liste, Diagnose_df):

        "Gir de ulike pasietenen en trafikklysgradering ut fra diagnosen de har"

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

        "Konverterer string til numeriskverid da dette var lettere å håndtere senere i koden"

        for pasient in pasient_liste:
            if pasient.tid == 'Dag':
                pasient.tid = 1
            elif pasient.tid == 'Tidlig Kveld':
                pasient.tid = 2
            elif pasient.tid == 'Kveld':
                pasient.tid = 3
            elif pasient.tid == 'Natt':
                pasient.tid = 4

    def legge_til_uker(self, pasient_liste):

        "Denne gir pasientene i listen et tilfeldig uketall mellom 1-4"

        counter = 1

        for month in range(1, 13):
            for day in range(7):
                dag = []
                tidligkveld = []
                kveld = []
                natt = []
                slutt_liste = []

                for pasient in pasient_liste:

                    if pasient.month == month:

                        if pasient.ukedag == day:

                            if not pasient.behandlet:

                                if pasient.tid == 1:
                                    dag.append(pasient)

                                elif pasient.tid == 2:
                                    tidligkveld.append(pasient)

                                elif pasient.tid == 3:
                                    kveld.append(pasient)

                                elif pasient.tid == 4:
                                    natt.append(pasient)

                dag.sort(key=lambda x: x.hast_nummer, reverse=True)
                tidligkveld.sort(key=lambda x: x.hast_nummer, reverse=True)
                kveld.sort(key=lambda x: x.hast_nummer, reverse=True)
                natt.sort(key=lambda x: x.hast_nummer, reverse=True)

                slutt_liste.extend(dag)
                slutt_liste.extend(tidligkveld)
                slutt_liste.extend(kveld)
                slutt_liste.extend(natt)

                for i in slutt_liste:
                    i.uke = counter

                    if counter < 4:
                        counter += 1
                    else:
                        counter = 1
