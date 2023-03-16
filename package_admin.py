from random import choice

class Package():
    def __init__(self, id, zipNumber, blockNumber, streetAddress, houseNumber):
        self.id = id
        self.zipNumber = None
        self.blockNumber = None
        self.streetAddress = None
        self.houseNumber = None
        
#Agregar que regrese paquetes entregados y paquetes activos
class PackageAdmin():
    ZIP_CODES = ["27018", "44789", "89943"]
        
    def __init__(self, packagesLimit = 10):
        self.packagesLimit = packagesLimit
        self.packagesToDeliver = []
        self.houses = []
        self.ordersAdm = {
        
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
        selectedPackages = []
        
        #traverse
        #travers packages to deliver
        
        #look for packages until we fill the delivery vehicle or we run out of packages
        while(selectedPackagesNumber < limit and len(self.packagesToDeliver) > 0):
            
            #traverse packages to deliver FIFO
            for i in range(0,len(self.packagesToDeliver),-1): #O(n), total packages
                
                #select package
                package = self.packagesToDeliver[i]
                
                #get package address information
                packageZipNum = package.zipNumber
                packageBlockNum = package.blockNumber
                packageStreetAddress = package.streetAddress
                
                #add package to selscted packages for current delivery
                selectedPackages.append(package) #add to packages to deliver
                selectedPackagesNumber += 1 #increment packages selected indicator
                
                #remove package from packages
                self.removePackage(package)
                
                #Select packages near the current package delivery zone
                #Look for packages in the same street
                for p in self.ordersAdm[packageZipNum][packageBlockNum][packageStreetAddress]: #O(n), total packages
                    
                    #check we have not reached limit and there exists packages to be delivered
                    if(selectedPackagesNumber < limit and len(self.packagesToDeliver) > 0):
                    
                        #add package
                        selectedPackages.append(p) #add to packages to deliver
                        selectedPackagesNumber += 1 #increment packages selected indicator
                        #remove package from packages
                        self.removePackage(p) #O(n)
                    else:
                        break
                    
                #Look for packages in the same block
                for street, packages in self.ordersAdm[packageZipNum][packageBlockNum].items(): #O(1), always 4 streets
                    
                    #we skip current street
                    if(street != packageStreetAddress):
                        
                        #check packages on each street
                        for p in packages: #O(n), total packages
                        
                            #check we have not reached limit and there exists packages to be delivered
                            if(selectedPackagesNumber < limit and len(self.packagesToDeliver) > 0):

                                #add package
                                selectedPackages.append(p) #add to packages to deliver
                                selectedPackagesNumber += 1 #increment packages selected indicator
                                #remove package from packages
                                self.removePackage(p) #O(n)  
                            else:
                                break
                        
                #Look for packages in the same zipCode 
                for block, streets in self.ordersAdm[packageZipNum].items(): #O(1) checking 2 blocks always
                    
                    #skip block we have already checked
                    if(block != packageBlockNum):
                        
                        #on each street
                        for street in streets: #O(1) checking 4 streets always
                            
                            #look for packages
                            for p in street: #O(n), number of packages 
                            
                                if(selectedPackagesNumber < limit and len(self.packagesToDeliver) > 0):
        
                                    #add package
                                    selectedPackages.append(p) #add to packages to deliver
                                    selectedPackagesNumber += 1 #increment packages selected indicator
                                    #remove package from packages
                                    self.removePackage(p) #O(n)    
                                else:
                                    break                       

                # #Look for packages in the map
                # #zipCode search ordering
                # zipCodes = list(packageZipNum)
                
                # for zipCode in self.ZIP_CODES:
                #     if zipCode != packageZipNum:
                #         zipCodes.append(zipCode)
                        
                # #zip code
                # for zipCode in zipCodes: #O(1), only 3 zipCodes
                #     #block
                #     for block in self.ordersAdm[zipCode].values(): #O(1), only 3 blocks per zip Code
                #         #Street
                #         for street in self.ordersAdm[zipCode][block].values(): #O(1), only 4 streets per block
                #             #order
                #             for p in street: #O(n), total packages
                                        
                #                 if(selectedPackages < self.packagesLimit and self.packagesToDeliverNumber != len(self.packagesToDeliver)):
                                    
                #                     #add package
                #                     selectedPackages.append(package) #add to packages to deliver
                #                     selectedPackagesNumber += 1 #increment packages selected indicator
                                    
                #                     #remove package from packages
                #                     self.removePackage(p) #O(n)
        
        return selectedPackages                          
            
    def removePackage(self, package):
        
        #remove from list of packages to be delivered
        self.packagesToDeliver.pop(package) #O(n) total packages
        
        #remove from orders administration
        self.ordersAdm[package.zipNumber][package.blockNumber][package.streetAddress].pop(package) #O(n)
        
    def createHouseOrder(self):
        
        #select random house
        house = choice(self.houses)
        
        #create order
        order = house.create_order()
        
        #add order
        self.packagesToDeliver.insert(0, order) #packagesToDeliver, O(n)
        self.ordersAdm[house.zipNumber][house.blockNumber][house.streetAddress].append(order)