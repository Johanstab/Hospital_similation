# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'


class TrafikkLys:

    def __init__(self, RedTid, YellowTid, GreenTid ):

        """

        :param RedTid:
        :param YellowTid:
        :param GreenTid:
        """

        self.red = RedTid
        self.yellow = YellowTid
        self.green = GreenTid
