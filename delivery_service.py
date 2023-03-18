from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
import numpy as np

#Agents and classes
from package_admin import Package, PackageAdmin
from house import House
from delivery_car import DeliveryCar
from traffic_manager import TrafficManager

#Map information
import map_code.map_data
import map_code.map_misc
from map_code.map import Map

import uuid
from random import choice


        
class DeliveryService(Model): 
    def __init__(self, street_positons, congested, house_positions, grid, graph, dispatch_coord, dispatch_street, car_capacity, num_cars = 1, optimized = True): 
        self.grid = grid
        self.grid_width = len(grid)
        self.grid_height = len(grid[0])
        self.mesa_grid = SingleGrid(self.grid_width, self.grid_height, False)
        self.sim_activation = SimultaneousActivation(self)
        self.map = Map(graph)
        self.dispatch_coord = dispatch_coord
        self.dispatch_street = dispatch_street
        self.datacollector = DataCollector(
            model_reporters={"Grid": self.get_grid}
        )

        #self.traffic_manager = TrafficManager(self.map, street_positons, congested, 10, 40)
        self.package_admin = PackageAdmin()

        self.sim_data = {}
        self.step_count = 0 

        self.place_houses(house_positions)

        self.carsDelivering = [] # car delivering
        self.carsAvailable = True
        self.deliveryCars = {}


    def place_houses(self, house_positions): 
        for pos in house_positions: 
            #print(house_positions[pos])
            houseInfo = list(house_positions[pos])
            a = House(uuid.uuid4(), self, str(houseInfo[0]), str(houseInfo[1]), str(houseInfo[2]), houseInfo[3])
            #print(a)
            self.mesa_grid.place_agent(a, pos)
            self.sim_activation.add(a)
            self.package_admin.houses.append(a)
            
    def get_grid(self):
        # Generamos la grid para contener los valores
        grid = np.zeros((self.grid_width, self.grid_height))

        return grid
    
    def is_intersection(self, x, y): 
        return self.grid[x][y] == 0
    
    def intersection_occupied(self, x, y): 
        analysis_radius = 1
        neighbours_radius_coordinates  = [[-1, -1], [-1, 0], [-1, 1],[0,-1],[0,0],[0,1],[1,-1],[1,0],[1,1]]
        for x_mod, y_mod in neighbours_radius_coordinates:
            if 0 < x + x_mod < self.grid_width and 0 < y + y_mod < self.grid_height: 
                if isinstance(self.mesa_grid[x + x_mod][y + y_mod], DeliveryCar) and self.grid[x + x_mod][y + y_mod] == 0: 
                    return True 
                
        for mod in range(analysis_radius * -1, analysis_radius + 1):
            if 0 < x + mod < self.grid_width and 0 < y + mod < self.grid_height and mod != 0: 
                if isinstance(self.mesa_grid[x + mod][y + mod], DeliveryCar) and self.grid[x + mod][y + mod] == 0: 
                    return True 
            
        return False 

    def car_coordinates(self): 
        coordinates = {}
        for car in self.carsDelivering:
            coordinates[car.unique_id] = self.deliveryCars[car.unique_id]
        # for car_id in self.deliveryCars:
        #     coordinates[car_id] = self.deliveryCars[car_id].pos

        return coordinates
    
    def num_delivered(self): 
        return self.orders.num_delivered()
    
    def in_bounds(self, x, y): 
        return 0 < x < self.grid_width and 0 < y < self.grid_height
            
    def step(self): 
        #self.traffic_manager.step()
        self.datacollector.collect(self)
        
        
        #Crear paquete cada 10 frames
        #if(self.step_count % 2 == 0):
            #Se crea orden en casa aleatoria
            #create package
        self.package_admin.createHouseOrder()
        # print(self.package_admin.ordersAdm)
        # print("==")
        # print(self.package_admin.packagesToDeliver)
        # print("=======")

        # Crear delivery cada 30 pasos
        if self.step_count % 30 == 0:
            # Verificar que la celda esté vacía
            x, y = self.dispatch_coord
            
            if self.mesa_grid.is_cell_empty(self.dispatch_coord):
                # Crear el delivery
                toDeliver = self.package_admin.selectPackagesForDelivery() #conseguimos paquetes para entregar
                deliveryCar = DeliveryCar(str(uuid.uuid4()), self, 's', 10, self.dispatch_coord)
                self.deliveryCars[deliveryCar.unique_id] = deliveryCar
                deliveryCar.delivering = True #está entregando un paquete
                self.sim_activation.add(deliveryCar)
                
                #Asignar ruta
                streetsToDeliver = [package.streetAddress for package in toDeliver]
                deliveryCar.set_tour(toDeliver, self.map.get_directions_SM(self.dispatch_street, streetsToDeliver))

            else:
                print('No se puede crear delivery: celda ocupada')            
        # #Crear delivery, aquí pasamos los paquetes a los carros
        # if(self.step_count % 30 == 0):
            
        #     #Paquetes y auto
        #     toDeliver = self.package_admin.selectPackagesForDelivery() #conseguimos paquetes para entregar
        #     print("Instanciando")
        #     deliveryCar = DeliveryCar(str(uuid.uuid4()),self, 's', 10, self.dispatch_coord) #creamos el auto
            
            
        #     #Lo agrego a delivery cars
        #     self.deliveryCars[deliveryCar.unique_id] = deliveryCar
        #     deliveryCar.delivering = True #está entregando un paquete
        #     self.carsDelivering.append(deliveryCar) #se le agrega a la lista de carros haciendo delivery
            
                
        #     #Asignar ruta
            
        #     #conseguimos calles
        #     streetsToDeliver = [package.streetAddress for package in toDeliver]
            
        #     #Asignamos la ruta y paquetes
        #     deliveryCar.set_tour(toDeliver, self.map.get_directions_SM(self.dispatch_street, streetsToDeliver))
            
                  

        # for car in self.deliveryCars.values(): 
        #     if car.pos == None or (car.pos == self.dispatch_coord and car.loaded_packages == 0): 
        #         if self.package_admin.packagesLimit > 0: 
        #             to_deliver = self.orders.get_orders(self.deliveryCars[car_id].capacity)
        #             to_deliver_streets = [package.street for package in to_deliver]

        #             self.deliveryCars[car_id].set_tour(to_deliver, self.map.get_directions(self.dispatch_street, to_deliver_streets))
                    
        #             self.mesa_grid.place_agent(self.deliveryCars[car_id], self.dispatch_coord)

            
        self.sim_activation.step()
        self.sim_data[self.step_count] = {
            'positions': self.car_coordinates(),
            #'streets': self.traffic_manager().get_traffic(), 
            #'packages': self.package_admin.selectPackagesForDelivery()
            }
        self.step_count += 1

# Delivery service 
    # Mantiene:  
    # - Ordenes (Orders)
    # - Modificaciones en el trafico del mapa (TrafficManager)
    # - Carros en operacion

    # Envia a Unity, en cada paso: 
    # - La posición actual de cada carro mensajero (diccionario)
    # - El estado de cada casa: el número de pedidos pendientes por casa. 
    # - La cantidad de trafico por calle. 
    
print("Salu2")

test = DeliveryService(map_code.map_data.STREET_POSITIONS, ["Torreon"], map_code.map_data.HOUSE_POSITIONS, map_code.map_data.GRID, map_code.map_data.GRAPH, (0,11), "Ocaña", 5, 3, True)

i = 0
while(i < 29):
    i += 1
    test.step()