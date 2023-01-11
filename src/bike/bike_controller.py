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
        # Update bike battery
        self.bike.set_battery(self.bike.get_battery() - 0.2)

        # Check if bike is out of battery
        if self.bike.get_battery() <= 3:
            print("1")
            # Update bike status to out of battery
            self.bike.set_status(30)
            
            # Return True to signal the simulation to deactivate the bike
            return 30

        # Check if destination is reached
        if self.current_chapter >= len(self.chapters) - 1:
            print("2")

            # If bike is in a no riding/parking area
            if self.bike.get_status() == 21:
                print("3")

                # Set current chapter to first index
                self.current_chapter = 0

                # Reverse the trip
                self.chapters.reverse()

                # Return False to signal the simulation to not deactivate the bike
                return False

            # Update the bike with final destination
            status = self.bike.set_position(str(self.chapters[-1])[1:-1].replace(" ", ""))

            # Check if the bike status was changed
            if status:
                self.status_change(status)

            # Reset and reverse the trip
            self.chapters.reverse()

            # Update the bike status to available
            self.bike.set_status(10)

            self.current_chapter = 0
            print("4")

            # Return True to signal the simulation that the destination have been reached
            return 10

        # Update the bike's geo positional data
        status = self.bike.set_position(str(self.chapters[self.current_chapter])[1:-1].replace(" ", ""))

        # Check if the bike status was changed
        if status:
            self.status_change(status)
            print("5")

        # Increment the current chapter by the chapter jumper
        self.current_chapter += self.jump
        return False

    def status_change(self, status):
        """
        Update relative data when a status was changed in the bike
        """
        if status == 1:
            self.jump = 5
            self.set_speed(18)
            return
        if status < 20:
            self.jump = 3
            self.set_speed(10)
            return
        if status == 20:
            self.jump = 5
            self.set_speed(18)
            return
        if status == 30:
            self.jump = 1
            self.set_speed(0)
            return
        if status == 50:
            self.jump = 5
            self.set_speed(18)
            return

    def reverse_chapters(self):
        """
        Reverse a set of positional data, called when a trip is finished
        """
        # Reverse the array of geo positional data
        self.chapters.reverse()

        # Reset chapter counter
        self.current_chapter = 0

    def set_speed(self, speed):
        """
        Update the speed value
        """
        self.bike.set_speed(speed)

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
