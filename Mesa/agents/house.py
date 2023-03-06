from Mesa import Agent
import numpy as np
import uuid

class House(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.ordersId = []
        self.address = None

    def create_order(self):
        #Generate Id for order
        orderId = uuid.uuid4()

        #Add Id to orders list
        self.ordersId.append(orderId)

        #Add Id to global model orders list
        

    