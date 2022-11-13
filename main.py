"""

"""

from src.bike_controller import BikeHandler

class BikeSimulator:
    """
    
    """
    def __init__(self):
        """

        """
        self.bikes = []

    def add_bike(self, bike):
        """
        
        """
        self.bikes.append(BikeHandler(bike["position"], bike["speed"], bike["battery"], bike["status"], bike["max_speed"]))

    def tt(self):
        while self.bikes:
            inp = input()
            inp = inp.split("-")
            self.bikes[int(inp[0])].change_status(int(inp[1]))
            

bike_data = {
    "position": "malmö",
    "speed": 15,
    "battery": 87,
    "status": 0,
    "max_speed": 20
}

# bike_data2 = {
#     "position": "lund",
#     "speed": 13,
#     "battery": 15,
#     "status": 0,
#     "max_speed": 20
# }

simulator = BikeSimulator()

simulator.add_bike(bike_data)
# simulator.add_bike(bike_data2)
simulator.tt()
