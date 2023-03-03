from mesa import Agent
import numpy as np

class House(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.orders = {}
        self.address = None

    def create_order(self):
        #Crear Id
        pass


    