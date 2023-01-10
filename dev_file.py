from src.simulation import Simulation

s = Simulation(host="http://localhost:4000/v1", udphost="localhost")
s.activation = True

s.start()