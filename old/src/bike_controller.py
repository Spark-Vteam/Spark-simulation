"""
Script for controlling the bike, calling functions and passing data.
"""
import requests

from src.bike import Bike
from src.repeated_timer import RepeatedTimer

class BikeHandler:
    """
    Class to control the bike
    """
    def __init__(self, id, position, speed, battery, status, max_speed=20):
        """
        Construct the BikeHandler and give it a bike
        """
        self.counter = 0
        self.rt = None
        self.destination = None
        self.bike = Bike(id, position, speed, battery, status, max_speed)
        self.change_status(int(status))

    def change_status(self, status):
        """
        Update the bike status
        """
        self.bike.set_status(status)
        print(self.bike.status)

        if self.rt:
            self.rt.stop()
        if status == 10:
            self.rt = RepeatedTimer(2, self.spit_data)
            return
        if status >= 20:
            self.rt = RepeatedTimer(10, self.spit_data)
            return
        self.rt = RepeatedTimer(0.01, self.fetch_data)

    def change_position(self, position):
        """
        
        """
        self.bike.set_position(position)

    def get_position(self):
        """
        Return the bikes position
        """
        return self.bike.get_position()

    def spit_data(self):
        """
        Emit function to share the bike data
        """
        print(self.bike.send_data())

    def fetch_data(self):
        """
        NOT YET IMPLEMENTET
        """
        url = 'http://localhost:4000'
        response = requests.get(url)
        self.counter += 1
        print(self.counter)