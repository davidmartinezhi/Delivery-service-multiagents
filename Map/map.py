from edge import Edge 
from chooser import Chooser
from map_misc import build_set, build_graph, path_to_directions, random_words

class Map: 
    def __init__(self, y_inters, x_inters, blk_height, blk_width, street_names = None):
        required_streets = (y_inters * 2 * (x_inters - 1)) + (x_inters * 2 * (y_inters - 1))

        if street_names is None: 
            street_names = random_words(required_streets, 3, 6, True)
        
        self.street_names = build_set(street_names) 

        if self.street_names == None or len(self.street_names) < required_streets: 
            raise Exception("Secuencia de calles ingresada inválida")

        self.graph = build_graph(y_inters, x_inters, blk_height, blk_width, Chooser(street_names))

    def get_directions(self, init_street, streets_to_visit, max_visits = 1): 
        visits = {key: 0 for key in self.graph}
        curr_path = {'dis': 0, 'path': [init_street]}
        best_path = {'dis': float('inf'), 'path': None}

        self.get_directions_aux(init_street, streets_to_visit, 0, visits, max_visits, curr_path, best_path)
        
        return path_to_directions(best_path['path'])

    def get_directions_aux(self, init_street, streets_to_visit, num_visits, visits, max_visits, curr_path, best_path): 
        if curr_path['path'][-1] == init_street and num_visits == len(streets_to_visit) and curr_path['dis'] < best_path['dis']: 
            best_path['path'] = curr_path['path'].copy()
            best_path['dis'] = curr_path['dis']
            return 
        
        for adj in self.graph[curr_path['path'][-1]].items():
            if curr_path['dis'] + adj[1].get_w() < best_path['dis'] and visits[adj[0]] < max_visits: 
                curr_path['path'].append(adj[0])
                curr_path['dis'] += adj[1].get_w()
                visits[adj[0]] += 1

                if adj[0] in streets_to_visit and visits[adj[0]] - 1 == 0: 
                    num_visits += 1

                self.get_directions_aux(init_street, streets_to_visit, num_visits, visits, max_visits, curr_path, best_path)

                if adj[0] in streets_to_visit and visits[adj[0]] - 1 == 0: 
                    num_visits -= 1

                curr_path['path'].pop()
                curr_path['dis'] -= adj[1].get_w()
                visits[adj[0]] -= 1

    def mod_street(self, street_name, change):
        if street_name not in self.street_names: 
            raise Exception("Calle inválida")
        list(self.graph[street_name].values())[0].mod_w(change)

        for node in self.graph:
            if street_name in self.graph[node]: 
                self.graph[node][street_name].mod_w(change)

    def restore_street(self, street_name): 
        if street_name not in self.street_names: 
            raise Exception("Calle inválida")
        list(self.graph[street_name].values())[0].restore()

        for node in self.graph:
            if street_name in self.graph[node]: 
                self.graph[node][street_name].restore()

    def get_street_names(): 
        
        pass