from random import random, sample
from .map_dijkstra import min_dis_dijkstra
import math 

def mod_s_order(s_order): 
    a, b = sample(range(1, len(s_order) - 1), 2)
    s_order_copy = s_order.copy()
    s_order_copy[a], s_order_copy[b] = s_order_copy[b], s_order_copy[a]
    return s_order_copy

def find_s_order_dis(graph, s_order, pairs):
    dis = 0 

    for i in range(len(s_order) - 1):
        if (s_order[i], s_order[i+1]) not in pairs: 
            pairs[(s_order[i], s_order[i+1])] = min_dis_dijkstra(graph, s_order[i], s_order[i+1]) 
        dis += pairs[(s_order[i], s_order[i+1])]  

    return dis 

# Terminar ejecución si se han explorado todas las permutaciones. 
def find_best_s_order(graph, init_s_order, init_temp = 1 * 10**100, end_temp = 0.1, cool_factor = 0.95, num_restarts = 1): 
    get_prob = lambda diff, temp: math.exp(-diff/temp) 
    temp = init_temp
    pairs = {}
    curr_s_order = {'dis': find_s_order_dis(graph, init_s_order, pairs), 's_order': init_s_order}
    best_s_order = curr_s_order

    for _ in range(num_restarts): 
        while temp > end_temp: 
            modified_s_order = mod_s_order(curr_s_order['s_order'])
            new_s_order = {'dis': find_s_order_dis(graph, modified_s_order, pairs), 's_order': modified_s_order}

            diff = new_s_order['dis'] - curr_s_order['dis']
            if  diff < 0 or random() < get_prob(diff, temp): 
                curr_s_order = new_s_order
                best_s_order = new_s_order if new_s_order['dis'] < best_s_order['dis'] else best_s_order
            
            temp *= cool_factor
            #num_iter += 1
        
        temp = init_temp
        curr_s_order = best_s_order

    return curr_s_order['s_order']
            