from queue import Queue
from .edge import Edge
from itertools import cycle, islice 

def rel_dir(coord_a, coord_b): 
    x_dif = coord_a[0] - coord_b[0]
    y_dif = coord_a[1] - coord_b[1]

    if x_dif != 0: 
        return 'w' if x_dif > 0 else 'e'
    elif y_dif != 0:
        return 's' if y_dif > 0 else 'n'

def build_grid(y_inters, x_inters, blk_height, blk_width): 
    grid_height = (y_inters - 1) * blk_height + y_inters * 2
    grid_width = (x_inters - 1) * blk_width + x_inters * 2

    street_col = list(islice(cycle([0] * 2 + [1] * blk_height), grid_height))
    block_front_col = list(islice(cycle([1] * 2 + [-1] + [2] * (blk_height-2) + [-1]), grid_height))
    block_col = list(islice(cycle([1] * 2 + [2] + [-1] * (blk_height - 2) + [2]), grid_height))

    return list(islice(cycle([street_col] * 2 + [block_front_col] + [block_col] * (blk_width - 2) + [block_front_col]), grid_width))

def get_adj_intersecs(curr_intersec, y_inters, x_inters):
    adj_intersecs = []
    for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0)]: 
        if 0 <= curr_intersec[0] + x < x_inters and 0 <= curr_intersec[1] + y < y_inters:
            adj_intersecs.append((curr_intersec[0]+x, curr_intersec[1]+y))

    return adj_intersecs

def build_graph(y_inters, x_inters, blk_height, blk_width, street_vertices):
    required_streets = (y_inters - 1) * (x_inters - 1) * 4 + ((y_inters - 1) + (x_inters - 1)) * 2
    if len(street_vertices) < required_streets: 
        raise Exception()

    intersecs = Queue()
    intersecs.put((0,0))
    in_queue = set()
    in_queue.add((0,0))
    graph = {}

    while not intersecs.empty(): 
        curr_intersec = intersecs.get()
        adj_intersecs = get_adj_intersecs(curr_intersec, y_inters, x_inters)
        graph[curr_intersec] = {}

        for adj in adj_intersecs: 
            w = blk_height/2 if rel_dir(curr_intersec, adj) == 'n' or rel_dir(curr_intersec, adj) == 's' else blk_width/2
            graph[curr_intersec][street_vertices[(curr_intersec, adj)]] = Edge(w)
            graph[street_vertices[(curr_intersec, adj)]] = {adj: Edge(w)}

        for adj in adj_intersecs: 
            if adj not in in_queue: 
                intersecs.put(adj)
                in_queue.add(adj)

    return graph

def print_graph(graph): 
    for node in graph: 
        print(f"{node}: ", end="")
        for adj in graph[node]: 
            print(f"{adj}({graph[node][adj].get_w()}) ", end="")
        print()

def my_range(inf, sup): # Ambos exclusivos 
    if inf < sup: 
        return range(inf + 1 , sup)
    elif inf > sup: 
        return range(inf - 1, sup, -1)
    return None

def place_block(house_data, block_number, corners, streets): 
    hor_line = lambda coord_a, coord_b: [(x, coord_a[1]) for x in my_range(coord_a[0], coord_b[0])]
    ver_line = lambda coord_a, coord_b: [(coord_a[0], y) for y in my_range(coord_a[1], coord_b[1])]
    house_num = 1

    for i in range(len(streets)): 
        if i % 2 == 0: 
            line = hor_line(corners[i], corners[(i+1) % len(streets)])
        else: 
            line = ver_line(corners[i], corners[(i+1) % len(streets)])

        for pos in line:             
            if(block_number == 1 or block_number == 2 or block_number == 4):
                zipNum = "27018"
            elif(block_number == 5 or block_number == 6 or block_number == 3):
                zipNum = "44789"
            elif(block_number == 7 or block_number == 8 or block_number == 9):
                zipNum = "89943"
            
            house_data[pos] = (zipNum, str(block_number), streets[i], house_num)
            house_num += 1