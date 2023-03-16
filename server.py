from flask import Flask 
from mesa_dir.model import DeliveryService 

app = Flask(__name__)

@app.route('/run_simulation/<num_packages>/<base_traffic>')
def run_simulation(num_packages, base_traffic): 
    delivery_service = DeliveryService(...)

    while delivery_service().num_delivered() < num_packages: 
        delivery_service.step()

    return delivery_service.get_sim_data()

