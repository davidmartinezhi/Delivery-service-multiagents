from map_misc_fun import build_grid, build_graph, place_block

y_inters = 4 
x_inters = 4 
blk_length = 5  

street_names = {
    # Arriba -> abajo
    ((1, 3), (0, 3)): 'Torreon', ((2, 3), (1, 3)): 'Francisco', ((3, 3), (2, 3)): 'Jorge', 
    ((0, 3), (1, 3)): '1N', ((1, 3), (2, 3)): '2N', ((2, 3), (3, 3)): '3N', 

    ((1, 2), (0, 2)): '1S', ((2, 2), (1, 2)): '2S', ((3, 2), (2, 2)): '3S', 
    ((0, 2), (1, 2)): '4N', ((1, 2), (2, 2)): '5N', ((2, 2), (3, 2)): '6N', 

    ((1, 1), (0, 1)): '4S', ((2, 1), (1, 1)): '5S', ((3, 1), (2, 1)): '6S', 
    ((0, 1), (1, 1)): '7N', ((1, 1), (2, 1)): '8N', ((2, 1), (3, 1)): '9N', 

    ((1, 0), (0, 0)): '7S', ((2, 0), (1, 0)): '8S', ((3, 0), (2, 0)): '9S', 
    ((0, 0), (1, 0)): 'Sam', ((1, 0), (2, 0)): 'Mayu', ((2, 0), (3, 0)): 'Esteban', 

    # Izquierda -> derecha
    ((0, 1), (0, 0)): 'Rodrigo', ((0, 2), (0, 1)): 'Ocaña', ((0, 3), (0, 2)): 'Roomba', 
    ((0, 0), (0, 1)): '7W', ((0, 1), (0, 2)): '4W', ((0, 2), (0, 3)): '1W', 

    ((1, 1), (1, 0)): '7E', ((1, 2), (1, 1)): '4E', ((1, 3), (1, 2)): '1E', 
    ((1, 0), (1, 1)): '8W', ((1, 1), (1, 2)): '5W', ((1, 2), (1, 3)): '2W', 

    ((2, 1), (2, 0)): '8E', ((2, 2), (2, 1)): '5E', ((2, 3), (2, 2)): '2E', 
    ((2, 0), (2, 1)): '9W', ((2, 1), (2, 2)): '6W', ((2, 2), (2, 3)): '3W', 

    ((3, 1), (3, 0)): '9E', ((3, 2), (3, 1)): '6E', ((3, 3), (3, 2)): '3E', 
    ((3, 0), (3, 1)): 'Daniel', ((3, 1), (3, 2)): 'David', ((3, 2), (3, 3)): 'Bolivia', 
}

STREETS = list(street_names.values())
GRAPH = build_graph(y_inters, x_inters, blk_length, blk_length, street_names)
GRID = build_grid(y_inters, x_inters, blk_length, blk_length) 
HOUSE_POSITIONS = {}

place_block(HOUSE_POSITIONS, 1, [(2, 20), (6, 20), (6, 16), (2, 16)], ['1N', '1E', '1S', '1W'])
place_block(HOUSE_POSITIONS, 2, [(9, 20), (13, 20), (13, 16), (9, 16)], ['2N', '2E', '2S', '2W'])
place_block(HOUSE_POSITIONS, 3, [(16, 20), (20, 20), (20, 16), (16, 16)], ['3N', '3E', '3S', '3W'])

place_block(HOUSE_POSITIONS, 4, [(2, 13), (6, 13), (6, 9), (2, 9)], ['4N', '4E', '4S', '4W'])
place_block(HOUSE_POSITIONS, 5, [(9, 13), (13, 13), (13, 9), (9, 9)], ['5N', '5E', '5S', '5W'])
place_block(HOUSE_POSITIONS, 6, [(16, 13), (20, 13), (20, 9), (16, 9)], ['6N', '6E', '6S', '6W'])

place_block(HOUSE_POSITIONS, 7, [(2, 6), (6, 6), (6, 2), (2, 2)], ['7N', '7E', '7S', '7W'])
place_block(HOUSE_POSITIONS, 8, [(9, 6), (13, 6), (13, 2), (9, 2)], ['8N', '8E', '8S', '8W'])
place_block(HOUSE_POSITIONS, 9, [(16, 6), (20, 6), (20, 2), (16, 2)], ['9N', '9E', '9S', '9W'])
