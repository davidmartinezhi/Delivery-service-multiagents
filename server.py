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
                                       (10, 30),
                                       int(car_capacity),
                                       int(num_cars),
                                       False if int(optimized) == 0 else True)

    while delivery_service.get_num_steps() < int(num_steps): 
        delivery_service.step()

    return delivery_service.get_sim_data()