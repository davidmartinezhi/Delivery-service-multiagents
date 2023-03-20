# Mesa 
from mesa import Model
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation

# Agents
from house import House
from delivery_car import DeliveryCar

from package_admin import PackageAdmin
from traffic_manager import TrafficManager
from map_code.map import Map
from traffic_manager import TrafficManager

# Misc
import uuid

class DeliveryService(Model): 
    def __init__(self, streets, congested, house_data, grid, graph, packages_rate, car_capacity, num_cars = 1, optimized = True): 
        self.grid = grid
        self.grid_width = len(grid)
        self.grid_height = len(grid[0])
        self.mesa_grid = SingleGrid(self.grid_width, self.grid_height, False)
        self.sim_activation = SimultaneousActivation(self)
        self.map = Map(graph)

        self.dispatch_coord = (0, 11)
        self.dispatch_street = 'Ocaña'
        self.dispatch_direction = 's'

        self.package_rate = packages_rate
        self.optimized = optimized

        self.traffic_manager = TrafficManager(self.map, streets, congested, 10, 40)
        self.package_admin = PackageAdmin()

        self.sim_data = {'steps': []}
        self.num_steps = 0 
        self.place_houses(house_data)

        self.deliveryCars = {i:DeliveryCar(uuid.uuid4(), self, car_capacity) for i in range(num_cars)}

    def place_houses(self, house_data): 
        for pos in house_data: 
            a = House(uuid.uuid4(), self, pos, *house_data[pos])
            self.mesa_grid.place_agent(a, pos)
            self.sim_activation.add(a)
            self.package_admin.houses.append(a) 
    
    def is_intersection(self, x, y): 
        return self.grid[x][y] == 0
    
    def intersection_occupied(self, x, y):         
        for neigh in self.mesa_grid.get_neighbors((x, y), True): 
            if isinstance(neigh, DeliveryCar) and self.is_intersection(neigh.pos[0], neigh.pos[1]): 
                return True 
        return False 

    def in_bounds(self, x, y): 
        return 0 < x < self.grid_width and 0 < y < self.grid_height
    
    def get_num_steps(self):
        return self.num_steps
    
    def get_car_positions(self): 
        return [{'carId': car_id, 'coord': car.pos} for car_id, car in self.deliveryCars.items() if car.pos != None]
    
    def get_streets(self): 
        streets = [{'streetName': street, 'traffic': traffic}
                   for street, traffic in self.traffic_manager.get_traffic().items()]

    def get_houses(self):
        return [{'houseCoord': coord, 'numPackages': num_packages}
                for coord, num_packages in self.package_admin.housesWithPendingPackages().items()]

    def build_step_data(self):
        step_data = {}
        step_data['positions'] = self.get_car_positions()
        step_data['streets'] = self.get_streets()
        step_data['houses'] = self.get_houses()
        return step_data
    
    def get_sim_data(self): 
        return self.sim_data
        
    def step(self): 
        self.traffic_manager.step()

        num_packages, per_step = self.package_rate
        if self.num_steps % per_step == 0: 
            self.package_admin.createHousePackages(num_packages)

        for car in self.deliveryCars.values(): 
            dc_x, dc_y = self.dispatch_coord
            if car.pos == None and self.mesa_grid[dc_x][dc_y] == None and self.package_admin.numPackagesToDeliver() > 0: 
                self.mesa_grid.place_agent(car, self.dispatch_coord)
                self.sim_activation.add(car)
                car.curr_direction = self.dispatch_direction
                car.active = False 

            if len(car.packages) == 0 and car.pos == self.dispatch_coord:
                car.active = False 
                if self.package_admin.numPackagesToDeliver() > 0:
                    packages = self.package_admin.selectPackagesForDelivery(car.capacity) 
                    if self.optimized: 
                        directions = self.map.get_directions_SM(self.dispatch_street, [p.streetAddress for p in packages.values()])
                    else: 
                        directions = self.map.get_directions_naive(self.dispatch_street, [p.streetAddress for p in packages.values()])
                    car.set_tour(packages, directions)
                    car.active = True 
        
        self.sim_data['steps'].append(self.build_step_data())
        self.sim_activation.step()
        self.num_steps += 1