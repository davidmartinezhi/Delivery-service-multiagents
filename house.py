import uuid
from mesa import Agent
from package_admin import Package

class House(Agent):
    def __init__(self, unique_id, model, houseCoord, zipNumber, blockNumber, streetAddress, houseNumber):
        super().__init__(unique_id, model)
        self.houseCoord = houseCoord
        self.zipNumber = zipNumber
        self.blockNumber = blockNumber
        self.streetAddress = streetAddress
        self.houseNumber = houseNumber

        self.packages = {}
        
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
    
    def remove_package(self, order_id): 
        self.packages.pop(order_id, None)

    def create_package(self):
        #Generate new package
        package = Package(uuid.uuid4(), self.houseCoord, self.zipNumber, self.blockNumber, self.streetAddress, self.houseNumber)
        
        #Add new package to packages delivered and assigned false since it has not been delivered
        self.packages[package.id] = package

        #return package
        return package