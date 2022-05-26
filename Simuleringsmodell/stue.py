# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'


class Stue:

    "Setter opp operasjonsstuene og tiden som er tilgjengelig i de ulike skiftene"

    def __init__(self, navn, hoytid=False):

        self.navn = navn

        if not hoytid:
            self.skift_1 = 480 * 1.1 # Dag skiftet er fra 07:30 til 15:30 og utgjør 480 min.
            self.skift_2 = 150 * 1.1 # Tidligkveld skiftet er fra 15:30 til 18:00 og utgjør 150 min.
            self.skift_3 = 270 * 1.1 # Kveld skiftet er fra 18:00 til 22:30 og utgjør 270 min.
            self.skift_4 = 540 * 1.1 # Natt skiftet er fra 22:30 til 07:30 og utgjør 540 min.

        else:# Denne skulle egentlig brukes til å håndterer mindre kapasitet i ferie uker, men ble ikke tatt i bruk
            self.skift_1 = 4000 * 4
            self.skift_2 = 800  * 4
            self.skift_3 = 1000 * 4
            self.skift_4 = 400  * 4

    def get_time(self, skift):

        "Henter tiden som er standard for gjeldene skift"

        if skift == 1:
            return self.skift_1
        elif skift == 2:
            return self.skift_2
        elif skift == 3:
            return self.skift_3
        elif skift == 4:
            return self.skift_4

    def fast_tid(self, skift):

        "For at simulerings filen skal kjøre er man avhengig av å kunne hente ut totalt skifttid som en statisk verdi"

        if skift == 1:
            return 480 * 1.1
        elif skift == 2:
            return 150 * 1.1
        elif skift == 3:
            return 270 * 1.1
        elif skift == 4:
            return 540 * 1.1

    def fast_tid_delt(self, skift):

        "Denne brukes ikke da den ble laget for det første logikken av modellen"

        if skift == 1:
            return 480 * 1.1
        elif skift == 2:
            return 150 * 1.1
        elif skift == 3:
            return 270 * 1.1
        elif skift == 4:
            return 540 * 1.1

    def update(self, skift, value):
        " Håndterer oppdateringen av tiden på stuene når en operasjon blir utført"
        if skift == 1:
            self.skift_1 += -value - 45
        elif skift == 2:
            self.skift_2 += -value - 30
        elif skift == 3:
            self.skift_3 += -value - 30
        elif skift == 4:
            self.skift_4 += -value - 30

    def reset_stue(self, hoytid=False):

        "Resetter tilgjengelig stuetid på starten av en neste dag"

        if not hoytid:
            self.skift_1 = 480 * 1.1
            self.skift_2 = 150 * 1.1
            self.skift_3 = 270 * 1.1
            self.skift_4 = 540 * 1.1

    def test_time(self,skift, value):

        "Ble laget for å teste logikk, ble ikke brukt i slutt koden."

        tid_1 = self.skift_1
        tid_2 = self.skift_2
        tid_3 = self.skift_3
        tid_4 = self.skift_4

        if skift == 1:
            tid_1 += -value - 45
            return  tid_1
        elif skift == 2:
            tid_2 += -value - 30
            return tid_2
        elif skift == 3:
            tid_3 += -value - 30
            return tid_3
        elif skift == 4:
            tid_4 += -value - 30
            return tid_4

