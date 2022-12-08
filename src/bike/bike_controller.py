"""
Script for controlling the bike, calling functions and passing data.
"""
import requests
import json

from src.bike.bike import Bike

class BikeHandler:
    """
    Class to control the bike
    """
    def __init__(self, id, position, speed, battery, status, max_speed=20):
        """
        Construct the BikeHandler and give it a bike
        """
        self.destination = None
        self.bike = Bike(id, position, speed, battery, status, max_speed)
        self.status = "idle"
        self.chapters = []
        self.current_chapter = 0

    def set_chapters(self, chapters):
        """
        Set chapters
        """
        self.chapters = chapters

    def read_chapter(self):
        """
        Read a chapter
        """
        if self.current_chapter == len(self.chapters) - 1:
            self.current_chapter = 0
        
        self.change_position(str(self.chapters[self.current_chapter])[1:-1])
        print(self.get_data())
        self.emit_data()

        self.current_chapter += 1

    def change_status(self, status):
        """
        Update the bike status
        """
        self.bike.set_status(status)

    def change_position(self, position):
        """
        
        """
        self.bike.set_position(position)

    def get_position(self):
        """
        Return the bikes position
        """
        return self.bike.get_position()

    def get_data(self):
        """
        Return all bike data
        """
        return self.bike.get_data()

    def emit_data(self):
        """
        Emit function to share the bike data
        """
        data = self.bike.get_data()

        res = requests.post("http://localhost:4000/bike/" + str(data["bikeId"]), json=data)