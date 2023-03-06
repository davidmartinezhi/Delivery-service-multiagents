from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

from Agents import House, Field

import numpy as np
import pandas as pd

class Mapa(Model):

    def __init__(self, width=20, height=20):
        self.grid= SingleGrid(width, height, True)

        for cell in self.grid.coord_iter():
            agent, x , y = cell
            if mat[x][y] == 2:
                self.grid.place_agent(House, (x, y))

            elif mat[x][y]== 0:
                self.grid.place_agent(Field, (x, y))
                