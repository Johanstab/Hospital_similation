# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'


class Stue:

    def __init__(self, navn, hoytid=False):

        self.navn = navn

        if not hoytid:
            self.skift_1 = 480 * 4.3 #Vi ganger med 4 siden det er 4 av hver ukedag i hver måned. Vi går bare gjennom ukedagne 1 gang for hver måned
            self.skift_2 = 150 * 4.3
            self.skift_3 = 270 * 4.3
            self.skift_4 = 540 * 4.3

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
            return 480 * 4.3
        elif skift == 2:
            return 150 * 4.3
        elif skift == 3:
            return 270 * 4.3
        elif skift == 4:
            return 540 * 4.3

    def fast_tid_delt(self, skift):

        if skift == 1:
            return 480
        elif skift == 2:
            return 150
        elif skift == 3:
            return 270
        elif skift == 4:
            return 540

    def update_tid(self, value, skift):
        if skift == 1:
            self.skift_1 += -value - 45
        elif skift == 2:
            self.skift_2 += -value - 45
        elif skift == 3:
            self.skift_3 += -value - 45
        elif skift == 4:
            self.skift_4 += -value - 45
