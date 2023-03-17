from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from itertools import permutations

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

        #self.traffic_manager = TrafficManager(self.map, street_positons, congested, 10, 40)
        self.package_admin = PackageAdmin()

        self.sim_data = {}
        self.step_count = 0 

        self.place_houses(house_positions)

        self.deliveryCars = {car_id: DeliveryCar(car_id, self, [], []) for car_id in range(num_cars)}
        for car in self.deliveryCars.values(): 
            self.sim_activation.add(car)

    def place_houses(self, house_positions): 
        for pos in house_positions: 
            #print(house_positions[pos])
            houseInfo = list(house_positions[pos])
            a = House(uuid.uuid4(), self, str(houseInfo[0]), str(houseInfo[1]), str(houseInfo[2]), houseInfo[3])
            #print(a)
            self.mesa_grid.place_agent(a, pos)
            self.sim_activation.add(a)
            self.package_admin.houses.append(a)

    def is_intersection(self, x, y): 
        return self.grid[x][y] == 0
    
    def intersection_occupied(self, x, y): 
        analysis_radius = 1

        for x_mod, y_mod in permutations(range(analysis_radius * -1, analysis_radius + 1)):
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
        for car_id in self.deliveryCars:
            coordinates[car_id] = self.deliveryCars[car_id].pos

        return coordinates
    
    def num_delivered(self): 
        return self.orders.num_delivered()
            
    def step(self): 
        #self.traffic_manager.step()
        
        #Crear paquete cada 10 frames
        #if(self.step_count % 2 == 0):
            #Se crea orden en casa aleatoria
            #create package
        self.package_admin.createHouseOrder()
        # print(self.package_admin.ordersAdm)
        # print("==")
        # print(self.package_admin.packagesToDeliver)
        # print("=======")
            
        #Crear delivery
        if(self.step_count % 10 == 0):
            print(self.package_admin.ordersAdm)
            toDeliver = self.package_admin.selectPackagesForDelivery()
            print("===")
            print("To Deliver: ",toDeliver)
            print("=======")
            print(self.package_admin.ordersAdm)
            pass
            

        for car in self.deliveryCars.values(): 
            if car.pos == None or (car.pos == self.dispatch_coord and car.loaded_packages == 0): 
                if self.package_admin.get_num_orders() > 0: 
                    to_deliver = self.orders.get_orders(self.deliveryCars[car_id].capacity)
                    to_deliver_streets = [package.street for package in to_deliver]

                    self.deliveryCars[car_id].set_tour(to_deliver, self.map.get_directions(self.dispatch_street, to_deliver_streets))
                    
                    self.mesa_grid.place_agent(self.deliveryCars[car_id], self.dispatch_coord)

        
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

test = DeliveryService(map_code.map_data.STREET_POSITIONS, ["Torreon"], map_code.map_data.HOUSE_POSITIONS, map_code.map_data.GRID, map_code.map_data.GRAPH, (0,11), "Ocaña", 5, 2, True)

i = 0
while(i < 11):
    i += 1
    test.step()