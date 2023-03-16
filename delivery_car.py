from mesa import Agent

class DeliveryCar(Agent): 
    def __init__(self, unique_id, model, listaPedidos, listaIndicaciones, limite = 10):
        super().__init__(unique_id, model)
        self.pedidos = listaPedidos
        self.indicaciones = listaIndicaciones
        self.limitePedidos = limite

        self.entregados = 0
        self.next_state = None
        self.index_indicaciones = 0

        self.pos = unique_id
        self.next_pos = None

    def nextHouse(self):
        direction = self.indicaciones[self.index_indicaciones]
        [x, y] = self.pos

        if (direction == 'N'):
            x = x + 1
        elif (direction == 'S'):
            x = x - 1
        elif (direction == 'E'):
            y = y - 1
        elif (direction == 'W'):
            y = y + 1

        return [x, y]

    def advance(self):
        [x,y] = self.nextHouse(self)

        nextHouse = self.model.grid[x][y]
        newListPedidos = []

        for pedido in self.pedidos:
            if pedido.houseNumber == nextHouse.houseNumber and pedido.streetAddress == nextHouse.streetAddress:
                entregados = entregados + 1
            else:
                newListPedidos.append(pedido)

        self.pedidos = newListPedidos

        self.grid.move_agent(self, self.next_pos)

    def normal_move(self, x, y):
        index_actual = self.indicaciones[self.index_indicaciones]
        if(index_actual == "N"):
            y = y + 1
        elif(index_actual == "W"):
            x = x - 1
        elif(index_actual == "E"):
            x = x + 1
        elif(index_actual == "S"):
            y = y - 1

    def intersection_move(self, x, y):
        index_actual = self.indicaciones[self.index_indicaciones]
        index_siguiente = self.indicaciones[self.index_indicaciones+1]

        if(index_actual == 'N'):
            y = y + 1
            if(index_siguiente == 'S'):
                x = x - 1
            elif(index_siguiente == 'W'):
                y = y + 1
        elif(index_actual == 'W'):
            x = x - 1
            if(index_siguiente == 'E'):
                y = y - 1
            elif(index_siguiente == 'S'):
                x = x - 1
        elif(index_actual == 'E'):
            x = x + 1
            if(index_siguiente == 'W'):
                y = y + 1
            elif(index_siguiente == 'N'):
                x = x + 1
        elif(index_actual == 'S'):
            y = y - 1
            if(index_siguiente == 'N'):
                x = x + 1
            elif(index_siguiente == 'E'):
                y = y - 1

    def choose_next_pos(self):
        x = self.pos[0]
        y = self.pos[1]

        if("intersection_zone"):
            self.normal_move(self, x, y)
        else:
            self.intersection_move(self, x, y)
        
        return (x,y)

    def step(self):
        if(not "interseccionOcupada" and not "otroCarro"):
            self.next_pos = self.choose_next_pos(self)

    def set_tour(self, orders, directions):
        self.pedidos = orders
        self.indicaciones = directions