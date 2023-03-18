import uuid
from mesa import Model, Agent
from package_admin import Package

class House(Agent):
    def __init__(self, unique_id, model, zipNumber, blockNumber, streetAddress, houseNumber):
        super().__init__(unique_id, model)
        self.ordersDelivered = dict()
        self.zipNumber = zipNumber
        self.blockNumber = blockNumber
        self.streetAddress = streetAddress
        self.houseNumber = houseNumber
        
    def __repr__(self):
        
        house = "Id: " + str(self.unique_id) + "\n"
        house = house + "Zip code: " + self.zipNumber + "\n"
        house = house + "Block: " + self.blockNumber + "\n"
        house = house + "Street: " + self.streetAddress + "\n"
        house = house + "Number: " + str(self.houseNumber) + "\n"
        return house

    def __str__(self):
        
        house = "id: " + str(self.unique_id) + "\n"
        house = house + "Zip code: " + self.zipNumber + "\n"
        house = house + "Block: " + self.blockNumber + "\n"
        house = house + "Street: " + self.streetAddress + "\n"
        house = house + "Number: " + str(self.houseNumber)
        return house

    def create_order(self):
        #Generate new order
        order = Package(uuid.uuid4(), self.zipNumber, self.blockNumber, self.streetAddress, self.houseNumber)
        
        #Add new order to orders delivered and assigned false since it has not been delivered
        self.ordersDelivered[order] = False

        #return order
        return order