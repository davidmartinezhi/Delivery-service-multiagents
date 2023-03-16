from queue import PriorityQueue

class Vertex_D: 
    def __init__(self, v, vertices):
        self.v = v
        self.dis = vertices[v]['dis']

    def __lt__(self, vertex_d):
        return self.dis < vertex_d.dis
    
def build_path_dijkstra(v_start, v_curr, vertices, path, exclude_start = True): 
    if v_curr == None or (v_curr == v_start and exclude_start): 
        return path 
    build_path_dijkstra(v_start, vertices[v_curr]['prev'], vertices, path)
    path.append(v_curr)
    
def min_path_dijkstra(graph, v_start, v_end, exclude_start = True):
    vertices = {v: {'dis': float('inf'), 'prev': None, 'visited': False} for v in graph} 
    queue = PriorityQueue()

    for v in graph: 
        queue.put(Vertex_D(v, vertices))

    vertices[v_start]['dis'] = 0
    queue.put(Vertex_D(v_start, vertices))
    v = queue.get().v

    while not queue.empty() and v != v_end and vertices[v]['dis'] != float('inf'): 
        for adj in graph[v]: 
            dis = vertices[v]['dis'] + graph[v][adj].get_w()
            if dis < vertices[adj]['dis'] and not vertices[adj]['visited']: 
                vertices[adj] = {'dis': dis, 'prev': v, 'visited': False}
                queue.put(Vertex_D(adj, vertices))

        v = queue.get().v
    
    path = []
    build_path_dijkstra(v_start, v_end, vertices, path, exclude_start)
    return path

def min_dis_dijkstra(graph, v_start, v_end): 
    vertices = {v: {'dis': float('inf'), 'visited': False} for v in graph} 
    queue = PriorityQueue()

    for v in graph: 
        queue.put(Vertex_D(v, vertices))

    vertices[v_start]['dis'] = 0
    queue.put(Vertex_D(v_start, vertices))
    v = queue.get().v

    while not queue.empty() and v != v_end and vertices[v]['dis'] != float('inf'): 
        for adj in graph[v]: 
            dis = vertices[v]['dis'] + graph[v][adj].get_w()
            if dis < vertices[adj]['dis'] and not vertices[adj]['visited']: 
                vertices[adj] = {'dis': dis, 'visited': False}
                queue.put(Vertex_D(adj, vertices))

        v = queue.get().v
    
    return vertices[v_end]['dis']