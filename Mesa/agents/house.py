from mesa import Agent
import uuid

class House(Agent):

    def __init__(self, model, zipNumber, blockNumber, streetAddress, houseNumber):
        super().__init__(model)
        self.ordersDelivered = dict()
        self.zipNumber = None
        self.blockNumber = None
        self.streetAddress = None
        self.houseNumber = None

    def create_order(self):
        #Generate new order
        order = Package(uuid.uuid4(), self.zipNumber, self.blockNumber, self.streetAddress, self.houseNumber)
        
        #Add new order to orders delivered and assigned false since it has not been delivered
        self.orders += {order: False}

        #return order
        return order