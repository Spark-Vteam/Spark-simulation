"""
Main script for Spark bike rental simulation
"""
import random

from src.bike_controller import BikeHandler
from src.repeated_timer import RepeatedTimer
from src.scenarios import Scenarios

class BikeSimulator:
    """
    
    """
    def __init__(self):
        """
        Constructor to initiate a simulation
        """
        self.bikes = [] # List to hold all BikeHandlers
        self.rt = None # Attribute to host the thread that generates scenarios
        self.pulse_timer = 10 # Time rate to execute scenario generating
        self.scenarios = Scenarios() # Scenarios instance, holds logic for the outcomes

    def add_bike(self, bike):
        """
        Add a BikeHandler to it's list
        """
        self.bikes.append(
            BikeHandler(
                bike["id"],
                bike["position"],
                bike["speed"],
                bike["battery"],
                bike["status"],
                bike["max_speed"]
                )
            )

    def initiate_bikes(self):
        """
        *** PLACEHOLDER FUNCTION / NOT YET IMPLEMENTED***
        Fetch all bikes from the database, format them and initiate them as Bike objects.
        """
        # Make a fetch
        bikes = [] # Place fetch in list
        for bike in bikes: # Go through every bike
            self.add_bike(bike) # Create a Bike object

    def simulator(self):
        """
        Main simulation function. Every x seconds it goes through every bike and generates a scenario.
        """
        for bike in self.bikes: # Go through every bike
            self.scenarios.generate_scenario(bike) # Generate a scenario for the current bike
       
# Mock data
bike_data = {
    "id": "0",
    "position": "55.609718195959864,13.000229772341523",
    "speed": 15,
    "battery": 87,
    "status": 20,
    "max_speed": 20
}

# Mock data
bike_data2 = {
    "id": "1",
    "position": "55.609718195959864,13.000229772341523",
    "speed": 13,
    "battery": 15,
    "status": 20,
    "max_speed": 20
}

simulator = BikeSimulator() # Create a simulator instance

simulator.add_bike(bike_data) # Add mock
simulator.add_bike(bike_data2) # Add mock
simulator.rt = RepeatedTimer(simulator.pulse_timer, simulator.simulator) # Initiate the simulator thread
