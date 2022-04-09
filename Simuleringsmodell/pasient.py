# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langaas@nmbu.no'


class Pasient:

    def __init__(self, PasientNr, Diagnose, Tidspunkt, Operasjonstype, TidOperasjon):

        self.pasientNr = PasientNr
        self.diagnose = Diagnose
        self.tidspunkt = Tidspunkt
        self.operasjonstype = Operasjonstype
        self.tidOperasjon = TidOperasjon
        self.ventetid = 0

    def oppdatere_ventetid(self, tid):
        self.ventetid = tid