# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'


class Stue:

    def __init__(self, navn, hoytid=False):

        self.navn = navn

        if not hoytid:
            self.skift_1 = 480 * 1.33
            self.skift_2 = 150 * 1.33
            self.skift_3 = 270 * 1.33
            self.skift_4 = 540 * 1.33

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
            return 480 * 1.33
        elif skift == 2:
            return 150 * 1.33
        elif skift == 3:
            return 270 * 1.33
        elif skift == 4:
            return 540 * 1.33

    def fast_tid_delt(self, skift):

        if skift == 1:
            return 480 * 1.33
        elif skift == 2:
            return 150 * 1.33
        elif skift == 3:
            return 270 * 1.33
        elif skift == 4:
            return 540 * 1.33

    def update(self, skift, value):
        if skift == 1:
            self.skift_1 += -value - 45
        elif skift == 2:
            self.skift_2 += -value - 30
        elif skift == 3:
            self.skift_3 += -value - 30
        elif skift == 4:
            self.skift_4 += -value - 30

    def reset_stue(self, hoytid=False):

        if not hoytid:
            self.skift_1 = 480 * 1.33
            self.skift_2 = 150 * 1.33
            self.skift_3 = 270 * 1.33
            self.skift_4 = 540 * 1.33

    def test_time(self,skift, value):

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

