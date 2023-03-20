from mesa import Agent
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

class DeliveryCar(Agent): 
    def __init__(self, unique_id, model, capacity):
        super().__init__(unique_id, model)
        self.model = model
        self.capacity = capacity
        self.queued_moves = Queue()

        self.pos = None
        self.curr_direction = None
        self.delivering = False
        self.queued_directions = Queue()
        self.packages = {}
        self.active = False 

    def turn_type(self, next_direction): 
        # Moving north
        if(self.curr_direction == "n"):
            return {'n': 'straight', 'e': 'right', 's': 'u-turn', 'w': 'left'}[next_direction]  
        # Moving east
        elif(self.curr_direction == "e"):
            return {'n': 'left', 'e': 'straight', 's': 'right', 'w': 'u-turn'}[next_direction]   
        # Moving west  
        elif(self.curr_direction == "w"):
            return {'n': 'right', 'e': 'u-turn', 's': 'left', 'w': 'straight'}[next_direction]                          
        # Moving south
        elif(self.curr_direction == "s"):
            return {'n': 'u-turn', 'e': 'left', 's': 'straight', 'w': 'right'}[next_direction] 
            
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
            positions.append(forward_pos(positions[-1], self.curr_direction))
            positions.append(left_pos(positions[-1], self.curr_direction))
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
        if self.active and self.queued_moves.empty(): 
            x_r, y_r = right_pos(self.pos, self.curr_direction)

            adj_house = self.model.mesa_grid[x_r][y_r] if self.model.in_bounds(x_r, y_r) else None 
                
            if isinstance(adj_house, House):
                for package_id in self.packages: 
                    if package_id in adj_house.packages: 
                        self.packages.pop(package_id)
                        adj_house.remove_package(package_id)
                        return 
                    
            x_f, y_f = forward_pos(self.pos, self.curr_direction)
            if self.model.is_intersection(x_f, y_f): 
                self.queue_turn_moves()
            else: 
                self.queue_forward_move()
        
    def advance(self):
        if not self.queued_moves.empty() and self.model.mesa_grid.is_cell_empty(self.queued_moves.queue[0]): 
            self.model.mesa_grid.move_agent(self, self.queued_moves.get())
