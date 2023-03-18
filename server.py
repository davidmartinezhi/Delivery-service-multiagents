from flask import Flask 
from delivery_service import DeliveryService 
from map_code.map_data import STREET_POSITIONS, GRAPH, GRID, HOUSE_POSITIONS 

app = Flask(__name__)

@app.route('/run_simulation/<num_packages>/<num_cars>/<car_capacity>/<optimized>')
def run_simulation(num_packages, num_cars, car_capacity, optimized): 
    delivery_service = DeliveryService(STREET_POSITIONS,
                                       ['4E', '5W', '5S', '8N', '2E', '3W'],
                                       HOUSE_POSITIONS,
                                       GRID, 
                                       GRAPH,
                                       (0, 11),
                                       'Ocaña',
                                       car_capacity,
                                       num_cars,
                                       False if optimized == 0 else True)

    while delivery_service().num_delivered() < num_packages: 
        delivery_service.step()

    return delivery_service.get_sim_data()

# {
#     1: {
#         'positions': {'carId': (0, 0)}, 
#         'streets': {'streetName': {'coord': (0, 0), 'trafficVal': 0}}, 
#         'houses': {house_id: {'coord': (0, 0), 'numPackages': 0}}
#     }
# }


