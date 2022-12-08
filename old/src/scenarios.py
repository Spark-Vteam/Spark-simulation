"""

"""

import random

class Scenarios:
    """
    This class creates a scenario for a given biken, the scenario is based on the data from the bike
    """

    def generate_scenario(self, bike):
        """
        Initiate generate scenario process
        """
        self.random_action(bike) # Randomize an action

    def random_action(self, bike):
        """
        With a random integer, the function rolls the dice to make a decision.
        """
        print("Running randomizer") # Confirmation
        res = random.randint(0,100) # Get a random integer

        # Make comparisons
        # /// CONSIDER CHANGING OUTCOMES TO 10, 20, 30 TO USE STATUS CODES INSTEAD ///
        if res >= 50:
            bike.change_status(10) # Update the status
            self.generate_rent(bike) # Create the scenario
            return
        bike.change_status(20) # Update the status

    def generate_rent(self, bike):
        """
        Create a rent. Calculate destination and update the BikeHandler
        """
        radius = 0.02 # In degrees, 0.02 is roughly 2.2KM
        position = bike.get_position().split(",") # Extract the positions
        destination_lat = random.uniform(float(position[0])-radius,float(position[0])+radius) # Calculate destination latitude based on radius from "radius" variable
        destination_lon = random.uniform(float(position[1])-radius,float(position[1])+radius) # Calculate destination longitude based on radius from "radius" variable
        bike.change_position(f"{destination_lat},{destination_lon}") # Update the BikeHandler
