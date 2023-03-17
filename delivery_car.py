from mesa import Agent, Model
from mesa.space import SingleGrid
from queue import Queue
from house import House

def forward_pos(pos, direction):
    x_mod = 1 if direction == 'e' else -1 if direction == 'w' else 0
    y_mod = 1 if direction == 'n' else -1 if direction == 's' else 0

    return pos[0] + x_mod, pos[1] + y_mod

def right_pos(pos, direction):
    x_mod = 1 if direction == 'n' else -1 if direction == 's' else 0
    y_mod = -1 if direction == 'e' else 1 if direction == 'w' else 0

    return pos[0] + x_mod, pos[1] + y_mod

def left_pos(pos, direction):
    x_mod = -1 if direction == 'n' else 1 if direction == 's' else 0
    y_mod = 1 if direction == 'e' else -1 if direction == 'w' else 0

    return pos[0] + x_mod, pos[1] + y_mod

def left_diag_pos(pos, direction): 
    if direction == 'n' or direction =='s': 
        x_mod = -1 if direction == 'n' else 1
        y_mod = 1 if direction == 'n' else -1
    else: 
        x_mod = -1 if direction == 'w' else 1
        y_mod = -1 if direction == 'w' else 1

    return pos[0] + x_mod, pos[1] + y_mod

class DeliveryCar(Agent): 
    def __init__(self, unique_id, model,  init_direction, capacity):
        super().__init__(unique_id, model)
        self.model = model
        self.curr_direction = init_direction
        self.capacity = capacity
        self.queued_moves = Queue()
        #self.delivery_service = delivery_service

        self.delivering = False
        self.queued_directions = None
        self.packages = []
        self.prev_house = None
        self.num_delivered = 0

    def turn_type(self, next_direction): 
        cardinal_dirs = {'n': 0, 'e': 1, 's': 2, 'w': 3}

        if next_direction == self.curr_direction: 
            return 'straight' 
        elif cardinal_dirs[next_direction] - cardinal_dirs[self.curr_direction] == 1: 
            return 'right'
        elif cardinal_dirs[next_direction] - cardinal_dirs[self.curr_direction] == -1: 
            return 'left'
        else: 
            return 'u-turn'
    
    def queue_forward_move(self):
        self.queued_moves.put(forward_pos(self.pos, self.curr_direction))

    def queue_turn_moves(self):
        positions = []
        positions.appeend(forward_pos(self.pos, self.curr_direction))
        next_direction = self.queued_directions.get()
        turn_t = self.turn_type()

        if turn_t == 'straight': 
            positions.append(forward_pos(positions[-1], self.curr_direction))
            positions.append(forward_pos(positions[-1], self.curr_direction))
        elif turn_t == 'right': 
            positions.append(right_pos(positions[-1], self.curr_direction))
        elif turn_t == 'left': 
            positions.append(left_diag_pos(positions[-1], self.curr_direction))
            positions.append(forward_pos(positions[-1], next_direction))
        else: 
            positions.append(left_pos(positions[-1], self.curr_direction))
            positions.append(forward_pos(positions[-1], next_direction))

        for pos in positions: 
            self.queued_moves.put(pos)
    
        self.curr_direction = next_direction

    def set_tour(self, packages, queued_directions):
        self.packages = packages
        self.queued_directions = queued_directions
    
    def step(self):
        
        if not self.queued_moves.empty(): 
            x_f, y_f = forward_pos(self.pos, self.curr_direction)
            if self.delivery_service.is_intersection(x_f, y_f): 
                self.queue_turn_moves()
            else: 
                self.queue_forward_move()
                
        else:
            self.delivering = False
    
    def advance(self):
        
        x_r, y_r = right_pos(self.pos, self.curr_direction)
        #print(self.model.grid_height)
        if (0 < x_r < self.model.grid_with and 0 < y_r < self.model.grid_height): 
            
            adj_house = self.model.grid[x_r][y_r]
            if isinstance(adj_house, House) and adj_house != self.prev_house: 
                packages_new = []
                for package in self.packages:
                    if package.houseNumber == adj_house.houseNumber and package.streetAddress == adj_house.streetAddress:
                        self.num_delivered += 1 
                    else:
                        packages_new.append(package)

                self.pedidos = packages_new
                self.prev_house = adj_house
                return 
            
        if self.model.intersection_occupied(self.pos[0], self.pos[1]): 
            return 
        
        x_f, y_f = forward_pos(self.pos, self.curr_direction)
        if self.model.grid[x_f][y_f] != None: 
            return 

        next_move = self.queued_moves.get()
        self.model.grid.move_agent(self, next_move)


        # Step: 
            # Calcular siguientes movimientos, si no hay movimientos pendientes. 
        # Advance: 
            # Mover el vehiculo a la siguiente posicón de la fila, si no se cumple lo siguiente: 
                # Obstrucción en el proximo movimiento. 
                # Intersección opcupada en el proximo movimiento. 
                # Entrega de paquete.