from mesa import Agent, Model
from mesa.space import SingleGrid
from queue import Queue
from house import House

def forward_pos(pos, direction):
    x_mod = 1 if direction == 'e' else -1 if direction == 'w' else 0
    y_mod = 1 if direction == 'n' else -1 if direction == 's' else 0
    
    newX = pos[0] + x_mod
    newY = pos[1] + y_mod
    return (newX, newY)

def right_pos(pos, direction):
    x_mod = 1 if direction == 'n' else -1 if direction == 's' else 0
    y_mod = -1 if direction == 'e' else 1 if direction == 'w' else 0
    print("Pos:",pos)
    
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
    def __init__(self, unique_id, model, init_direction, capacity, pos):
        super().__init__(unique_id, model)
        self.model = model
        self.curr_direction = init_direction
        self.capacity = capacity
        self.queued_moves = Queue()

        self.delivering = False
        self.queued_directions = None
        self.packages = []
        self.prev_house = None
        self.num_delivered = 0
        
        self.pos = pos
        self.model.mesa_grid.place_agent(self, pos)
        self.model.sim_activation.add(self)

    def turn_type(self, next_direction): 

        #moving north
        if(self.curr_direction == "n"):
            
            if(next_direction == "e"):
                return "right"
                
            elif(next_direction == "w"):
                return "left"
                
            elif(next_direction == "n"):
                return "straight"
                
            elif(next_direction == "s"):
                return "u-turn"
                
        #moving east
        elif(self.curr_direction == "e"):
            if(next_direction == "s"):
                return "right"
                
            elif(next_direction == "n"):
                return "left"
                
            elif(next_direction == "e"):
                return "straight"
                
            elif(next_direction == "w"):
                return "u-turn"
                      
        #moving west  
        elif(self.curr_direction == "w"):
            if(next_direction == "n"):
                return "right"
                
            elif(next_direction == "s"):
                return "left"
                
            elif(next_direction == "w"):
                return "straight"
                
            elif(next_direction == "e"):
                return "u-turn"
                        
        #moving south
        elif(self.curr_direction == "s"):
            
            if(next_direction == "w"):
                return "right"
                
            elif(next_direction == "e"):
                return "left"
                
            elif(next_direction == "s"):
                return "straight"
                
            elif(next_direction == "n"):
                return "u-turn"
    
    def queue_forward_move(self):
        self.queued_moves.put(forward_pos(self.pos, self.curr_direction))

    def queue_turn_moves(self):
        positions = []
        positions.append(forward_pos(self.pos, self.curr_direction))
        next_direction = self.queued_directions.get()
        turn_t = self.turn_type(next_direction)

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
        
        #Al inicio no tiene queued moves
        if self.queued_moves.empty(): 
            
            #sacamos siguiente paso a tomar
            print(self.curr_direction)
            x_f, y_f = forward_pos(self.pos, self.curr_direction)
            
            #Checamos si ese paso es dentro de la intersección
            if self.model.grid[x_f][y_f] == 0: # is intersection
                self.queue_turn_moves()
                
            #Si no esta en una intersección no se mueve
            else: 

                self.queue_forward_move()
                
        else:
            print("No queued moves")
                
    
    def advance(self):

        x_r, y_r = right_pos(self.pos, self.curr_direction)
        
        if (0 < x_r < self.model.grid_width and 0 < y_r < self.model.grid_height): 

            adj_house = self.model.grid[x_r][y_r]
            if isinstance(adj_house, House) and adj_house != self.prev_house: 
                packages_new = []
                for package in self.packages:
                    if package.houseNumber == adj_house.houseNumber and package.streetAddress == adj_house.streetAddress:
                        self.num_delivered += 1 
                       #adj_house.ordersDelivered[package.id] = True
                    else:
                        packages_new.append(package)

                self.pedidos = packages_new
                self.prev_house = adj_house
                return 
            
        # if self.model.intersection_occupied(self.pos[0], self.pos[1]): 
        #     return 
        
        x_f, y_f = forward_pos(self.pos, self.curr_direction)
        if self.model.grid[x_f][y_f] == isinstance(self.model.grid[x_f][y_f],DeliveryCar) or self.model.grid[x_f][y_f] == isinstance(self.model.grid[x_f][y_f],House): 
            return 

        next_move = self.queued_moves.get()
        self.model.mesa_grid.move_agent(self, next_move)


        # Step: 
            # Calcular siguientes movimientos, si no hay movimientos pendientes. 
        # Advance: 
            # Mover el vehiculo a la siguiente posicón de la fila, si no se cumple lo siguiente: 
                # Obstrucción en el proximo movimiento. 
                # Intersección opcupada en el proximo movimiento. 
                # Entrega de paquete.