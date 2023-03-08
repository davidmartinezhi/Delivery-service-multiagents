from queue import Queue
from map_misc_fun import rel_dir

def path_to_directions(path): 
    directions = Queue()
    from_inter = None

    for elem in path: 
        if isinstance(elem, tuple):
            if from_inter is not None: 
                directions.put(rel_dir(from_inter, elem))
            from_inter = elem

    return directions

class Map: 
    def __init__(self, graph):
        self.graph = graph

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
        if street_name not in self.graph: 
            raise Exception('Calle inexistente')
        
        list(self.graph[street_name].values())[0].mod_w(change)

        for node in self.graph:
            if street_name in self.graph[node]: 
                self.graph[node][street_name].mod_w(change)

    def restore_street(self, street_name): 
        if street_name not in self.graph: 
            raise Exception("Calle inexistente")
        
        list(self.graph[street_name].values())[0].restore()

        for node in self.graph:
            if street_name in self.graph[node]: 
                self.graph[node][street_name].restore()