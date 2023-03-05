from queue import Queue
from edge import Edge
from random import randint, choice

def build_set(seq): 
    if len(seq) == 0: 
        return None
    
    new_set = set()
    for elem in seq: 
        if elem in new_set: 
            return None
        new_set.add(elem)

    return new_set

def rel_dir(coord_a, coord_b): 
    x_dif = coord_a[0] - coord_b[0]
    y_dif = coord_a[1] - coord_b[1]

    if x_dif != 0: 
        return 'w' if x_dif > 0 else 'e'
    elif y_dif != 0:
        return 's' if y_dif > 0 else 'n'

def get_adj_intersecs(curr_intersec, y_inters, x_inters):
    adj_intersecs = []
    for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0)]: 
        if 0 <= curr_intersec[0] + x < x_inters and 0 <= curr_intersec[1] + y < y_inters:
            adj_intersecs.append((curr_intersec[0]+x, curr_intersec[1]+y))

    return adj_intersecs

def build_graph(y_inters, x_inters, blk_height, blk_width, street_names):
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
            street = street_names.choose()
            graph[curr_intersec][street] = Edge(w)
            graph[street] = {adj: Edge(w)}

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

def random_words(num_strings, min_size, max_size, capitalized=False):
    word = []
    words = []
    letters = [[97, 101, 105, 111, 117]]
    letters.append([dec for dec in range(97, 123) if dec not in letters[0]])
    probabilities = [[0]*80+[1]*20, [1]*80+[0]*20]

    for i in range(num_strings): 
        curr_prob = randint(0, 1)
        if capitalized:
            word.append(chr(choice(letters[choice(probabilities[curr_prob])]) - 32))
        else:
            word.append(chr(choice(letters[choice(probabilities[curr_prob])])))

        for _ in range(randint(min_size-1, max_size-1)): 
            curr_prob = (curr_prob + 1) % 2
            word.append(chr(choice(letters[choice(probabilities[curr_prob])])))

        words.append("".join(word))
        word.clear()

    return words 

def path_to_directions(path): 
    directions = Queue()

    for i in range(0, len(path) - 2, 2): 
        directions.put(rel_dir(path[i], path[i+2]))

    return directions