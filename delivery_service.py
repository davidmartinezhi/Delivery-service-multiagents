from mesa import Model
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from itertools import permutations

from map import Map
from traffic_manager import TrafficManager
        
class DeliveryService(Model): 
    def __init__(self, street_positons, congested, house_positions, grid, graph, dispatch_coord, dispatch_street, car_capacities, num_cars = 1): 
        self.grid = grid
        self.grid_width = len(grid)
        self.grid_height = len(grid[0])
        self.mesa_grid = SingleGrid(self.grid_width, self.grid_height, False)
        self.sim_activation = SimultaneousActivation()
        self.map = Map(graph)
        self.dispatch_coord = dispatch_coord
        self.dispatch_street = dispatch_street

        self.traffic_manager = TrafficManager(self.map, street_positons, congested, 10, 40)
        self.package_admin = PackageAdministrator()

        self.sim_data = {}
        self.step_count = 0 

        self.place_houses(house_positions)

        self.deliveryCars = {car_id: DeliveryCar(car_capacities[i]) for car_id in range(num_cars)}
        for car in self.deliveryCars.values(): 
            self.sim_activation.add(car)

    def place_houses(self, house_positions): 
        for pos in house_positions: 
            self.mesa_grid.place_agent(House(*house_positions[pos]), pos)
            self.sim_activation.add()

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
        self.traffic_manager.step()

        for car in self.deliveryCars.values(): 
            if car.pos == None or (car.pos == self.dispatch_coord and car.loaded_packages == 0): 
                if self.package_admin.get_num_orders() > 0: 
                    to_deliver = self.orders.get_orders(self.deliveryCars[car_id].capacity)
                    to_deliver_streets = [package.street for package in to_deliver]

                    self.deliveryCars[car_id].set_tour(to_deliver, self.map.get_directions(self.dispatch_street, to_deliver_streets))
                    
                    self.mesa_grid.place_agent(self.deliveryCars[car_id], self.dispatch_coord)

        self.sim_data[self.step_count] = {
            'positions': self.car_coordinates(),
            'streets': self.traffic_manager().get_traffic(), 
            'packages': self.package_admin.active_packages()}
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