"""
Script to voice the bike
"""

# Socket needed for communication with bike server
import socket
from shapely.geometry import Point, Polygon

class Bike:
    """
    The Bike class is the communicator between the
    physical hardware on the bike and the web based 
    database and clients.
    """

    def __init__(self, id, position, speed, battery, status, max_speed, HOST, PORT, geofences):
        """
        Constructor setting the correct, self explanatory,
        values on it's attributes.
        """
        # Initiate the Bike object with it's registered values
        self.id = id
        self.position = position
        self.speed = speed
        self.battery = battery
        self.status = status
        self.max_speed = max_speed
        self.geofences = geofences
        self.geofence = 0

        # Set UDP host address
        self.HOST = HOST

        # Set UDP port
        self.PORT = PORT

    def set_position(self, position):
        """
        Update the bike's geo positional data
        """
        # Variable to let the bike handler know if theres been a change in status
        status_changed = False

        # Function called by physical bike which also supplies the data
        self.position = position

        # Compare the new position with geofenced areas
        gf = self.check_geofence()

        # If a match, proceed
        if gf > 0 and gf != self.geofence:

            # Set status change check to True
            status_changed = gf

            # 10-19 is a slow zone where the second digit is the speed limit divided by 2
            if gf < 20:
                self.set_status(21)
                self.set_max_speed((gf-10)*2)

            # 20 is a no parking zone, the bike status 20 mean active while 21 mean active but not allowed to park
            elif gf < 30:
                self.set_status(22)

            # 30 is a no riding area
            elif gf < 40:
                self.set_max_speed(0)
                self.set_status(23)

            # 50 is a parking zone
            elif gf <= 50:
                self.set_status(24)

        elif gf == 0 and self.geofence != 0:
            # Set status change check to True
            status_changed = 1

            # Set status to current status without geofence addition
            self.set_status(round(self.status/10)*10)

            # Reset the geofence attribute
            self.geofence = 0

            # Set max speed to maximum
            self.max_speed = 18

        # Update geofence attribute
        self.geofence = gf

        # Emit the new data to the bike server
        self.emit_data()

        return status_changed

    def get_position(self):
        """
        Retrieve the geo positional data
        """
        # Returns its position attribute
        return self.position

    def set_speed(self, speed):
        """
        Set the bike's current speed
        """
        # Method called from the physical bike to update its current speed
        self.speed = speed

    def get_speed(self):
        """
        Retrieve the current speed
        """
        # Returns the current speed of the bike
        return self.speed

    def set_battery(self, battery):
        """
        Set the bike's battery level
        """
        # Check if battery is under the lower limit
        if battery <= 3:

            # status code30 -> battery <= 3%
            self.set_status(30)

        # Method called by physical bike to reflect remaining battery
        self.battery = battery

    def get_battery(self):
        """
        Retrieve current battery level
        """
        # Returns battery level
        return self.battery
    
    def set_status(self, status):
        """
        Set the bike status.
        """
        # Set the status code for the bike
        # 10 -> available
        # 20 -> active
        # 30 -> battery <= 3%
        # 40 -> maintenance needed

        self.status = status

        # When a new status is recieved, signal the lights to reflect status
        self.emit_lights(status)

    def get_status(self):
        """
        Retrieve the current status
        """
        # Returns the bike status
        return self.status

    def set_max_speed(self, max_speed):
        """
        Set the bikes max speed, (e.g. upon entering a specific zone),
        the bike's max speed can be lowered or increased.
        """
        # Set the max allowed speed
        self.max_speed = max_speed

    def get_max_speed(self):
        """
        Retrieve the max speed
        """
        # A method used by the physical bike to restrict motors max speed
        return self.max_speed

    def check_geofence(self, parking=False):
        """
        Check if bike is inside a geofenced area
        """
        pos = self.position.split(",")
        point = Point(float(pos[0]), float(pos[1]))
        for k,v in self.geofences.items():
            polygon = Polygon(v["Coordinates"])
            if point.within(polygon):
                return v["Type"]
        return 0
                    

    def emit_lights(self, status):
        """
        Activate the bike's lights
        """
        # A method used by the physical bikes to activate colored light depending on status
        # 10 -> GREEN
        # 20 -> BLUE
        # 30 -> RED
        # 40 -> YELLOW

        # Compare the status code to activate relevant color
        if status == 10:
            return "green"
        if status == 20:
            return "blue"
        if status == 30:
            return "red"
        return "yellow"

    def emit_data(self):
        """
        Emits the data to the bike server in order to update the database
        """
        # Format the data
        data = f"{self.id},'{self.position}',{self.battery},{self.status},{self.speed}"

        # Define the socket, in AF_INET is Internet while SOCK_DGRAM is UDP
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Send the message
        UDPClientSocket.sendto(str.encode(f"({data})"), (self.HOST,self.PORT))
