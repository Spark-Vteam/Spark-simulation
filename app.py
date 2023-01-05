from flask import Flask
from flask import request
from src.simulation import Simulation
from src.helpers.routing import generate_route
import threading




app = Flask(__name__)

sim = Simulation()

def worker():
    sim.start()
    return

t = threading.Thread(target=worker)
t.start()

def start():
    t = threading.Thread(target=worker)
    t.start()
    return "Simulation started"

@app.route('/')
def index():
    return "Flask server"

@app.route('/enable-activation')
def enable_activation():
    sim.activation = True

@app.route('/activate', methods=["POST"])
def activate():
    bike_id = request.form['bike_id']
    user_id = request.form['user_id']
    position = request.form['position']
    destination = request.form['destination']
    route = generate_route(position, destination)
    sim.activate_from_app(bike_id, user_id, route)

    return "Trip started"

@app.route('/stop/<bike_id>', methods=["PUT"])
def stop(bike_id):
    bike_index = sim.get_bike_index("active", bike_id)
    sim.deactivate_bike(bike_index)
    return f"Bike {bike_id} stopped"



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)