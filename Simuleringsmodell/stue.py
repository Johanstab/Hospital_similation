# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'


class Stue:

    def __init__(self, navn, hoytid=False):

        self.navn = navn

        self.skift_1 = 0
        self.skift_2 = 0
        self.skift_3 = 0
        self.skift_4 = 0

        if not hoytid:
            self.skift_1 = 480
            self.skift_2 = 150
            self.skift_3 = 270
            self.skift_4 = 540

        else:
            self.skift_1 = 4000 * 4
            self.skift_2 = 800  * 4
            self.skift_3 = 1000 * 4
            self.skift_4 = 400  * 4

    def get_time(self, skift):

        if skift == 1:
            return self.skift_1
        elif skift == 2:
            return self.skift_2
        elif skift == 3:
            return self.skift_3
        elif skift == 4:
            return self.skift_4

    def fast_tid(self, skift):

        if skift == 1:
            return 480
        elif skift == 2:
            return 150
        elif skift == 3:
            return 270
        elif skift == 4:
            return 540

    def fast_tid_delt(self, skift):

        if skift == 1:
            return 480
        elif skift == 2:
            return 150
        elif skift == 3:
            return 270
        elif skift == 4:
            return 540

    def update(self, skift, value):
        if skift == 1:
            self.skift_1 += -value - 45
        elif skift == 2:
            self.skift_2 += -value - 30
        elif skift == 3:
            self.skift_3 += -value - 30
        elif skift == 4:
            self.skift_4 += -value - 30

    def new_shift(self, skift):
        if skift == 2 and self.skift_1 > 0:
            self.skift_2 += self.skift_1
        elif skift == 3 and self.skift_2 > 0:
            self.skift_3 += self.skift_2

    def reset_stue(self, hoytid=False):

        if not hoytid:
            self.skift_1 = 480
            self.skift_2 = 150
            self.skift_3 = 270
            self.skift_4 = 540


