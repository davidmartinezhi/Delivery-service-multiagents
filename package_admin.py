from random import choice

class Package():
    def __init__(self, id, houseCoord, zipNumber, blockNumber, streetAddress, houseNumber):
        self.id = id
        self.houseCoord = houseCoord
        self.zipNumber = zipNumber
        self.blockNumber = blockNumber
        self.streetAddress = streetAddress
        self.houseNumber = houseNumber
        
    def __repr__(self):
        return str(self.id)
    
    def __str__(self):
        return str(self.id)
    
    def __eq__(self, package):
        return self.id == package.id
        
#Agregar que regrese paquetes entregados y paquetes activos
class PackageAdmin():
    ZIP_CODES = ["27018", "44789", "89943"]
        
    def __init__(self):
        self.packagesToDeliver = []
        self.houses = []
        self.packagesAdm = {
            #Zip Codes
            "27018": {
                #Blocks
                "1": {
                    #Streets with homes
                    "1W": [],
                    "1N": [],
                    "1E": [],
                    "1S": [],    
                },
                "2": {
                    #Streets with homes
                    "2W": [],
                    "2N": [],
                    "2E": [],
                    "2S": [],                           
                },
                "4":{
                    #Streets with homes
                    "4W": [],
                    "4N": [],
                    "4E": [],
                    "4S": [],   
                }
            },
            "44789": {
                    #Blocks
                    "5": {
                        #Streets with homes
                        "5W": [],
                        "5N": [],
                        "5E": [],
                        "5S": [],    
                    },
                    "6": {
                        #Streets with homes
                        "6W": [],
                        "6N": [],
                        "6E": [],
                        "6S": [],                           
                    },
                    "3":{
                        #Streets with homes
                        "3W": [],
                        "3N": [],
                        "3E": [],
                        "3S": [],   
                    }
            },
            "89943": {
                #Blocks
                "7": {
                    #Streets with homes
                    "7W": [],
                    "7N": [],
                    "7E": [],
                    "7S": [],    
                },
                "8": {
                    #Streets with homes
                    "8W": [],
                    "8N": [],
                    "8E": [],
                    "8S": [],                           
                },
                "9":{
                    #Streets with homes
                    "9W": [],
                    "9N": [],
                    "9E": [],
                    "9S": [],   
                }
            }
        }
           
    def selectPackagesForDelivery(self, limit = 10):
        selectedPackagesNumber = 0
        selectedPackages = {}
        
        #look for packages until we fill the delivery vehicle or we run out of packages
        if(len(self.packagesToDeliver) > 0):
            #traverse packages to deliver FIFO
            for package in self.packagesToDeliver: #O(n), total packages
                #get package address information
                packageZipNum = package.zipNumber
                packageBlockNum = package.blockNumber
                packageStreetAddress = package.streetAddress
                
                #add package to selected packages for current delivery
                selectedPackages[package.id] = package #add to packages to deliver
                selectedPackagesNumber += 1 #increment packages selected indicator
                self.removePackage(package) #remove package from packages
                
                #Select packages near the current package delivery zone
                #Look for packages in the same street
                for p in self.packagesAdm[packageZipNum][packageBlockNum][packageStreetAddress]: #O(n), total packages
                    #check we have not reached limit and there exists packages to be delivered
                    if(selectedPackagesNumber < limit and len(self.packagesToDeliver) > 0):
                        #add package
                        selectedPackages[p.id] = p #add to packages to deliver
                        selectedPackagesNumber += 1 #increment packages selected indicator
                        #remove package from packages
                        self.removePackage(p) #O(n)
                    else:
                        return selectedPackages
                    
                #Look for packages in the same block
                for street, packages in self.packagesAdm[packageZipNum][packageBlockNum].items(): #O(1), always 4 streets
                    #we skip current street
                    if(street != packageStreetAddress):
                        
                        #check packages on each street
                        for p in packages: #O(n), total packages
                        
                            #check we have not reached limit and there exists packages to be delivered
                            if(selectedPackagesNumber < limit and len(self.packagesToDeliver) > 0):

                                #add package
                                selectedPackages[p.id] = p #add to packages to deliver
                                selectedPackagesNumber += 1 #increment packages selected indicator
                                #remove package from packages
                                self.removePackage(p) #O(n)  
                            else:
                                return selectedPackages
                        
                #Look for packages in the same zipCode 
                for block, streets in self.packagesAdm[packageZipNum].items(): #O(1) checking 2 blocks always
                    
                    #skip block we have already checked
                    if(block != packageBlockNum):
                        
                        #on each street
                        for street in streets: #O(1) checking 4 streets always
                            
                            #look for packages
                            for p in self.packagesAdm[packageZipNum][block][street]: #O(n), number of packages 
                            
                                if(selectedPackagesNumber < limit and len(self.packagesToDeliver) > 0):
        
                                    #add package
                                    selectedPackages[p.id] = p #add to packages to deliver
                                    selectedPackagesNumber += 1 #increment packages selected indicator
                                    #remove package from packages
                                    self.removePackage(p) #O(n)    
                                else:
                                     return selectedPackages   
                                                            
        return selectedPackages                          
            
    def removePackage(self, package):
        #remove from list of packages to be delivered
        packageIdx = self.packagesToDeliver.index(package)
        self.packagesToDeliver.pop(packageIdx) #O(n) total packages
        
        #remove from orders administration
        ordersAdminPackageIdx = self.packagesAdm[package.zipNumber][package.blockNumber][package.streetAddress].index(package)
        self.packagesAdm[package.zipNumber][package.blockNumber][package.streetAddress].pop(ordersAdminPackageIdx) #O(n)
        
    def createHousePackages(self, numOrders = 1):
        for _ in range(numOrders): 
            #select random house
            house = choice(self.houses)
            
            #create package
            package = house.create_package()
            
            #add package
            self.packagesAdm[house.zipNumber][house.blockNumber][house.streetAddress].append(package)
            self.packagesToDeliver.append(package) #packagesToDeliver, O(n)

    def housesWithPendingPackages(self): # Returns a dictionary that associates a house coordiante with the number of packages
        # assigned to that house, for every house that is currently expecting a delivery: {'houseCoord': numPackages, ...}
        housesPenPackages = {}
        for house in self.houses: 
            if len(house.packages) > 0: 
                housesPenPackages[house.houseCoord] = len(house.packages)

        return housesPenPackages
            
    def numPackagesToDeliver(self): 
        return len(self.packagesToDeliver)