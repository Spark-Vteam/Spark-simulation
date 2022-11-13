"""
Script to voice the bike
"""

class Bike:
    """
    The Bike class is the communicator between the
    physical hardware on the bike and the web based 
    database and clients.
    """

    def __init__(self, position, speed, battery, status, max_speed):
        """
        Constructor setting the correct, self explanatory,
        values on it's attributes.
        """
        self.position = position
        self.speed = speed
        self.battery = battery
        self.status = status
        self.max_speed = max_speed
    
    def set_max_speed(self, max_speed):
        """
        Set the bikes max speed, (e.g. upon entering a specific zone),
        the bike's max speed can be lowered or increased.
        """
        self.max_speed = max_speed

    def set_status(self, status):
        """
        Set the bike status.
        """
        self.status = status

    def update_data(self, position, speed, battery):
        """
        Update the bike's position, speed and battery.
        These data fields are expected to be updated
        frequently during a ride.
        """
        self.position = position
        self.speed = speed
        self.battery = battery

    def send_data(self):
        """
        Return all data bound to the bike
        """
        data = {
            "position": self.position,
            "speed": self.speed,
            "battery": self.battery,
            "status": self.status,
            "max_speed": self.max_speed
        }

        return data
