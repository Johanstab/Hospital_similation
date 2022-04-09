# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'


class Pasient:

    def __init__(self, PasientNr, Diagnose, FagOmrade, Operasjonstype, Month, Ukedag, TidOperasjon):

        """

        :param PasientNr:
        :param Diagnose:
        :param Tidspunkt:
        :param Operasjonstype:
        :param TidOperasjon:
        """

        self.pasientNr = PasientNr
        self.diagnose = Diagnose
        self.fagOmrade = FagOmrade
        self.operasjonstype = Operasjonstype
        self.month = Month
        self.ukedag = Ukedag
        self.tidOperasjon = TidOperasjon
        self.ventetid = 0

    def oppdatere_ventetid(self, tid):
        self.ventetid = tid