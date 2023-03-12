from mesa import Agent 

class DeliveryCar(Agent): 
    def __init__(self, unique_id, model, listaPedidos, listaIndicaciones, limite):
        super().__init__(unique_id, model)
        self.pedidos = listaPedidos
        self.indicaciones = listaIndicaciones
        self.limitePedidos = limite

        self.entregados = 0
        self.next_state = None
        self.index_indicaciones = 0

        self.pos = unique_id
        self.next_pos = None

    def choose_next_pos(self):
        x = self.pos[0]
        y = self.pos[1]

        if("intersection_zone") {
            normal_move(self, x, y)
        } else {
            intersection_move(self, x, y)
        }
        return (x,y)

    def step(self):
        self.next_pos = self.choose_next_pos()

    def advance(self):
        neighbours = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False)

        for neighbor in neighbours:
            if pedidos[neighbor]:
                entregados = entregados + pedidos[neighbor].len()
                pedidos.pop(neighbor)

        self.grid.move_agent(self, self.next_pos)

    def normal_move(self, int x, int y):
        index_actual = self.indicaciones[self.index_indicaciones]
        if(index_actual == "N"):
            y = y + 1
        elif(index_actual == "W"):
            x = x - 1
        elif(index_actual == "E"):
            x = x + 1
        elif(index_actual == "S"):
            y = y - 1

    def intersection_move(self, int x, int y):
        index_actual = self.indicaciones[self.index_indicaciones]
        index_siguiente = self.indicaciones[self.index_indicaciones+1]

        if(index_actual == "N"):
            y = y + 1
            if(index_siguiente == "S"):
                x = x - 1
            elif(index_siguiente == "W"):
                y = y + 1
        elif(index_actual == "W"):
            x = x - 1
            if(index_siguiente == "E"):
                y = y - 1
            elif(index_siguiente == "S"):
                x = x - 1
        elif(index_actual == "E"):
            x = x + 1
            if(index_siguiente == "W"):
                y = y + 1
            elif(index_siguiente == "N"):
                x = x + 1
        elif(index_actual == "S"):
            y = y - 1
            if(index_siguiente == "N"):
                x = x + 1
            elif(index_siguiente == "E"):
                y = y - 1