# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'


class Stue:

    parametere = {}

    @classmethod
    def sett_parametere(cls, nye_parametere):
        for parameter in nye_parametere:
            if parameter not in cls.parametere:
                    raise KeyError('Parameteren eksisterer ikke:' + nye_parametere[0])

    def __init__(self):

        self.stuer = []


class OrtoStue(Stue):

    def __init__(self):
        super().__init__()


class RestStue(Stue):

    def __init__(self):
        super().__init__()
