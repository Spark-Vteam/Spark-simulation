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
    def __init__(self, num_bikes=10):
        """
        Constructor
        """
        self.idle_bikes = []
        self.num_bikes = num_bikes

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
        for i in range(self.num_bikes):
            self.idle_bikes[i].set_chapters(standard_trip(self.idle_bikes[i].get_position()))
            self.idle_bikes[i].change_status(20)

    def loop(self):
        """
        Test loop
        """
        for i in range(self.num_bikes):
            self.idle_bikes[i].read_chapter()

def main():
    """
    Main function
    """
    num_bikes = 10
    emit_frequency = 2
    df = DataFetcher("http://localhost:4000/")
    users = df.fetch("user")
    bikes = df.fetch("bike")

    S = Simulation(num_bikes)
    S.init_bikes(bikes)
    S.set_chapters()
    rt = RepeatedTimer(emit_frequency, S.loop)

if __name__ == '__main__':
    main()
