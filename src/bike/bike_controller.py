"""
Script for controlling the bike, calling functions and passing data.
"""
from src.bike.bike import Bike

class BikeHandler:
    """
    A bikehandler manipulates a Bike.

    Acts as a puppet master to the bike as
    it tells bike how to behave in a believable way.
    """
    def __init__(self, id, position, speed, battery, status, chapters, geofences, host):
        """
        Constructor
        """
        # Set the id
        self.id = id

        # Create a Bike object to control
        self.bike = Bike(id, position, speed, battery, status, 18, host, 9898, geofences)

        # Assign the generated route as chapters
        self.chapters = chapters

        # Decides which chapter to read, defaults to 0
        self.current_chapter = 0

        # Number of indexes in chapters to skip, controls speed, 5 = 18km/h while 3 = 10.2km/h
        self.jump = 5

        # Declare a user attribute
        self.user = 0

    def read_chapter(self):
        """
        Read a chapter, makes the bike take the next step of the simulated trip
        """
        try:
            # Update bike battery
            self.bike.set_battery(self.bike.get_battery() - 0.3)

            # Check if bike is out of battery
            if self.bike.get_battery() <= 3:

                # Update bike status to out of battery
                self.bike.set_status(30)
                
                # Return True to signal the simulation to deactivate the bike
                return 30

            # Check if destination is reached
            if self.current_chapter >= len(self.chapters) - 1:

                # Update the bike with final destination
                self.bike.set_position(str(self.chapters[-1])[1:-1].replace(" ", ""))

                # Reset and reverse the trip
                self.chapters.reverse()

                # Update the bike status to available
                self.bike.set_status(10)

                self.current_chapter = 0


                # Return True to signal the simulation that the destination have been reached
                return 10

            # Update the bike's geo positional data
            self.bike.set_position(str(self.chapters[self.current_chapter])[1:-1].replace(" ", ""))

            # Check if the chapter jump needs to be adjusted to a geofence interaction
            max_speed = self.bike.get_max_speed()

            if max_speed == 18:
                self.jump = 5
            elif max_speed == 10:
                self.jump = 3
                print(f"Bike: {self.id} in slow zone")
            elif max_speed == 0:
                print(f"Bike: {self.id} in no go zone")
                self.jump = 1 # walking speed

            # Increment the current chapter by the chapter jumper
            self.current_chapter += self.jump
            return False
        except TabError:
            self.change_status(50)
            return 50

    def reverse_chapters(self):
        """
        Reverse a set of positional data, called when a trip is finished
        """
        # Reverse the array of geo positional data
        self.chapters.reverse()

        # Reset chapter counter
        self.current_chapter = 0

    def change_status(self, status):
        """
        Update the bike status
        """
        self.bike.set_status(status)

    def set_user(self, user):
        """
        Set the user
        """
        self.user = user

    def get_user(self):
        """
        Get the user
        """
        return self.user

    def get_id(self):
        """
        Return the id
        """
        return self.id

    def get_position(self):
        """
        Return the bikes position
        """
        return self.bike.get_position()
