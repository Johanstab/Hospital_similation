# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'


class Pasient:

"Oppretter pasient objektet som brukes videre i simuleringen."

    def __init__(self, PasientNr, Diagnose, FagOmrade, Operasjonstype, Month, Ukedag, TidOperasjon,
                 Stuetid, ErOhjelp):
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
        self.tid = TidOperasjon
        self.erohjelp = ErOhjelp
        self.stuetid = Stuetid
        self.hast = None
        self.ventetid = 0
        self.nummer = None
        self.inntid = 0
        self.hast_nummer = 0
        self.behandlet = False
        self.uke = 0




