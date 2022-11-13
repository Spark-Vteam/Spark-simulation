"""
Script for controlling the bike, calling functions and passing data
"""
import requests

from src.bike import Bike
from src.repeated_timer import RepeatedTimer

class BikeHandler:
    """
    
    """
    def __init__(self, position, speed, battery, status, max_speed=20):
        """
        
        """
        self.counter = 0
        self.rt = None
        self.bike = Bike(position, speed, battery, status, max_speed)
        self.change_status(int(status))

    def change_status(self, status):
        """
        
        """
        if self.rt:
            self.rt.stop()
        if status == 10:
            self.rt = RepeatedTimer(2, self.spit_data)
            return
        if status >= 20:
            self.rt = RepeatedTimer(10, self.spit_data)
            return
        self.rt = RepeatedTimer(0.01, self.fetch_data)

    def spit_data(self):
        """
        
        """
        print(self.bike.send_data())

    def fetch_data(self):
        url = 'http://localhost:4000'
        response = requests.get(url)
        self.counter += 1
        print(self.counter)

    def run(self):
        """
        
        """
        rt = RepeatedTimer(5, self.spit_data)
