from mesa import Model
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from map import Map
from bridge import Bridge 
from itertools import permutations
from random import choice, choices, randint, random

class TrafficManager(): 
    def __init__(self, map, streets, congested, min_traffic, max_traffic, max_num_jams = 5, jam_prob = 0.1, phase_duration = 100): 
        self.map = map
        self.streets = streets
        self.congested_streets = congested
        self.min_traffic = min_traffic
        self.max_traffic = max_traffic
        self.max_num_jams = max_num_jams
        self.jam_prob = jam_prob
        self.phase_duration = phase_duration
        self.in_peak_traffic = False
        self.curr_step = -1

        self.affected_streets = {}
        
    def update_traffic(self): 
        for street in self.affected_streets.keys(): 
            self.map.restore_street(street)
            self.affected_streets[street].pop()

        if self.in_peak_traffic: 
            for street in self.congested_streets: 
                traffic = randint(self.min_traffic, self.max_traffic)
                map.mod_street(street, traffic)
                self.affected_streets[street] = traffic 

        for _ in self.max_num_jams: 
            if self.jam_prob <= random(): 
                self.affected_streets[choice(self.streets)] = self.max_traffic

    def get_traffic(self): 
        return self.affected_streets

    def step(self): 
        self.curr_step += 1
        if self.curr_step % self.phase_duration == 0: 
            self.in_peak_traffic = not self.in_peak_traffic
            self.update_traffic()
        
class DeliveryService(Model): 
    def __init__(self, streets, congested, house_positions, grid, graph, dispatch_coord, dispatch_street, car_capacities, num_cars = 1,): 
        self.grid = grid
        self.grid_width = len(grid)
        self.grid_height = len(grid[0])
        self.mesa_grid = SingleGrid(self.grid_width, self.grid_height, False)
        self.map = Map(graph)
        self.dispatch_coord = dispatch_coord
        self.dispatch_street = dispatch_street

        self.bridge = Bridge()
        self.traffic_manager = TrafficManager(self.map, streets, congested, 10, 40)
        self.orders = Orders()

        self.place_houses(house_positions)
        self.deliveryCars = {car_id: DeliveryCar(car_capacities[i]) for car_id in range(num_cars)}

    def place_houses(self, house_positions): 
        for pos in house_positions: 
            self.mesa_grid.place_agent(House(*house_positions[pos]), pos)

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
            
    def step(self): 
        self.traffic_manager.step()

        for car_id in self.deliveryCars: 
            if self.deliveryCars[car_id].pos == None: 
                if self.orders.get_num_orders() > 0: 
                    to_deliver = self.orders.get_orders(self.deliveryCars[car_id].capacity)
                    to_deliver_streets = [package.street for package in to_deliver]

                    self.deliveryCars[car_id].set_tour(to_deliver, self.map.get_directions(self.dispatch_street, to_deliver_streets))
                    
                    self.mesa_grid.place_agent(self.deliveryCars[car_id], self.dispatch_coord)

        self.bridge.send_data(self.car_coordinates(), self.orders.active_orders(), self.traffic_manager.get_traffic())
        
# Delivery service 
    # Mantiene:  
    # - Ordenes (Orders)
    # - Modificaciones en el trafico del mapa (TrafficManager)
    # - Carros en operacion

    # Envia a Unity, en cada paso: 
    # - La posición actual de cada carro mensajero (diccionario)
    # - El estado de cada casa: el número de pedidos pendientes por casa. 
    # - La cantidad de trafico por calle. 