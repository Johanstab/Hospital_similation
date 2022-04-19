# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'


class Stue:

    def __init__(self, navn, hoytid=False):

        self.navn = navn

        if not hoytid:
            self.skift_1 = 480 * 4 #Vi ganger med 4 siden det er 4 av hver ukedag i hver måned. Vi går bare gjennom ukedagne 1 gang for hver måned
            self.skift_2 = 150 * 4
            self.skift_3 = 270 * 4
            self.skift_4 = 540 * 4

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
            return 480 * 4
        elif skift == 2:
            return 150 * 4
        elif skift == 3:
            return 270 * 4
        elif skift == 4:
            return 540 * 4
