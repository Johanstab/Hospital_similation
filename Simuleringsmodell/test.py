# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'

import pandas as pd


class Stue:

    def __init__(self, fag, hoytid=False):

        self.hoytid = hoytid
        self.fag = fag

        if not hoytid:
            self.skift_1 = 4320 * self.fag.parametere['Dag'] * 4
            self.skift_2 = 1050 * self.fag.parametere['Tidlig kveld'] * 4
            self.skift_3 = 1350 * self.fag.parametere['Kveld'] * 4
            self.skift_4 = 480  * 4


        else:
            self.skift_1 = 4000
            self.skift_2 = 800
            self.skift_3 = 1000
            self.skift_4 = 400

    def get_time(self, skift):

        if skift == 1:
            return self.skift_1
        elif skift == 2:
            return self.skift_2
        elif skift == 3:
            return self.skift_3
        elif skift == 4:
            return self.skift_4

    def fast_tid(self,skift):

        if skift == 1:
            return 4320 * self.fag.parametere['Dag'] * 4
        elif skift == 2:
            return 1050 * self.fag.parametere['Tidlig kveld'] * 4
        elif skift == 3:
            return 1350 * self.fag.parametere['Kveld'] * 4
        elif skift == 4:
            return 480  * 4


