from src.simulation import Simulation

s = Simulation(host="http://localhost:4000/v1", udphost="localhost")
s.activation = True

s.start()

# for item in s.idle_bikes:
#     if len(item.chapters) < 10:
#         print(len(item.chapters), item.id)
