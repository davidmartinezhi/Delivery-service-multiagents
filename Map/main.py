from map import Map 
from map_misc import print_graph, random_words

map = Map(2, 5, 5, 100)
directions = map.get_directions((0, 0), [(1, 1), (3, 1), (1, 0)])

print_graph(map.graph)

while not directions.empty(): 
    print(directions.get())

