from flask import Flask 
from delivery_service import DeliveryService 
from map_code.map_data import STREET_NAMES, GRAPH, GRID, HOUSE_DATA

app = Flask(__name__)

@app.route('/run_simulation/<num_steps>/<num_cars>/<car_capacity>/<optimized>')
def run_simulation(num_steps, num_cars, car_capacity, optimized): 
    delivery_service = DeliveryService(STREET_NAMES,
                                       ['4E', '5W', '5S', '8N', '2E', '3W'],
                                       HOUSE_DATA,
                                       GRID, 
                                       GRAPH,
                                       (20, 20),
                                       int(car_capacity),
                                       int(num_cars),
                                       False if int(optimized) == 0 else True)

    while delivery_service.get_num_steps() < int(num_steps): 
        delivery_service.step()

    print(delivery_service.get_sim_data())
    return delivery_service.get_sim_data()

# ds = DeliveryService(STREET_NAMES, ['Ocaña', 'Daniel'], HOUSE_DATA, GRID, GRAPH, (5, 10), 5, 3, True)

# counter = 0 
# while ds.get_num_steps() < 300: 
#     ds.step()
#     print(counter)
#     counter += 1

# sim_data = ds.get_sim_data()
# positions = [step['positions'] for step in sim_data['steps']]

# for pos in positions: 
#     print(pos)
