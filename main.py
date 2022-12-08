"""
Main script for simulation
"""
from src.data.datafetcher import DataFetcher
from src.bike.bike_controller import BikeHandler
from src.scenarios.trip import standard_trip
from src.helpers.repeated_timer import RepeatedTimer
import polyline

url_update_bike = "http://localhost:4000/bike"

class Simulation:
    """
    Main simulator
    """
    def __init__(self):
        """
        Constructor
        """
        self.idle_bikes = []

    def init_bikes(self, bikes):
        """
        Create Bikehandlers and bikes from API result
        """
        for b in bikes:
            self.idle_bikes.append(BikeHandler(b["id"], b["Position"], b["Speed"], b["Battery"], b["Status"]))

    def set_chapters(self):
        """
        Set chapters for x bikes
        """
        for i in range(10):
            self.idle_bikes[i].set_chapters(standard_trip(self.idle_bikes[i].get_position()))

    def loop(self):
        """
        Test loop
        """
        for i in range(10):
            self.idle_bikes[i].read_chapter()

def main():
    """
    Main function
    """
    df = DataFetcher("http://localhost:4000/")
    users = df.fetch("user")
    bikes = df.fetch("bike")

    S = Simulation()
    S.init_bikes(bikes)
    S.set_chapters()
    rt = RepeatedTimer(2, S.loop)
    # df = DataFetcher("http://localhost:4000/")

    # users = df.fetch("user")
    # bikes = df.fetch("bike")
    
    # idle_bikes = []

    # for b in bikes:
    #     idle_bikes.append(BikeHandler(b["id"], b["Position"], b["Speed"], b["Battery"], b["Status"]))

    # for i in range(10):
    #     idle_bikes[i].set_chapters(standard_trip(idle_bikes[i].get_position()))

if __name__ == '__main__':
    main()
