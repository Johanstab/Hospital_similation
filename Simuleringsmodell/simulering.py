# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johan.stabekk@nmbu.no, sabina.langas@nmbu.no'

import pandas as pd

from pasient import Pasient
from stue import Stue
from trafikklys import TrafikkLys


class HospitalSim:

    def __init__(self, df):
        self.stue = Stue


