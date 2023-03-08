from mesa import Model
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from map import Map 

class DeliveryService(Model): 
    def __init__(self, grid, graph, streets, house_positions, dispatch_coord, num_cars = 1): 
        self.grid = grid
        self.map = Map(graph)
        self.streets = streets
        self.mesa_grid = SingleGrid(len(self.grid[0]), len(self.grid), False)
        self.place_houses(house_positions)
        self.orders = Orders()

    def place_houses(self, house_positions): 
        for pos in house_positions: 
            self.mesa_grid.place_agent(House(*house_positions[pos]), pos)

    def is_intersection(self, coord_x, coord_y): 
        return self.grid[coord_x][coord_y] == 0
    
    def dispatch_delivery_car(): 
        

