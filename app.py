from flask import Flask
from flask import request
from src.simulation import Simulation
from src.helpers.routing import generate_route
import threading
import polyline




app = Flask(__name__)

sim = Simulation()

def worker():
    sim.start()

def worker2():
    app.run(host='0.0.0.0', port=8000)

def worker3():
    sim.deactivate_all()

t = threading.Thread(target=worker)
t.start()

def start():
    t = threading.Thread(target=worker)
    t.start()
    return "Simulation started"

@app.route('/')
def index():
    return "Flask server"

@app.route('/sim_start')
def sim_start():
    if sim.read_active == False:
        return "Command failed, simulation is still shutting down"
        
    sim.activation = True

    return f"Starting simulation of activation"

@app.route('/activate/<bike_id>/<user_id>/<position>/<destination>')
def activate(bike_id, user_id, position, destination):
    route = generate_route(position, destination)
    sim.activate_from_app(bike_id, user_id, route)

    return "Trip started"

@app.route('/stop/<bike_id>')
def stop(bike_id):
    bike_index = sim.get_bike_index("active", bike_id)
    sim.deactivate_bike(bike_index, 10)
    return f"Bike {bike_id} stopped"

@app.route('/sim_stop')
def stop_sim():
    sim.activation = False
    sim.read_active = False

    t = threading.Thread(target=worker3)
    return "Simulation stopped"



if __name__ == '__main__':
	# app.run(host='0.0.0.0', port=8000)
    s = threading.Thread(target=worker2)
    s.start()