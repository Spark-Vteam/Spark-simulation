"""
Main script for simulation
"""
import time
import random
import polyline
from src.helpers.setup import *
from src.data.bikes import bikes
from src.data.users import users
from src.helpers.http import Http
from src.data.geofences import geofences
from src.helpers.timer import timer_output
from src.data.routes_encoded import routes
from src.bike.bike_controller import BikeHandler

class Simulation:
    """
    Main simulator
    """
    def __init__(self, emit_frequency=5, generate_data=False, activation_chance=0.01, host="http://server:4000/v1", udphost="bike-server"):
        """
        Constructor
        """
        # A switch to enable the activation iteration
        self.activation = False
        self.read_active = True

        # Set the interval for sending positional data to bike server
        self.emit_frequency = emit_frequency

        # Create a http service
        self.http = Http(host)

        # Set activation chance attribute
        self.activation_chance = activation_chance

        # Set counter of finished rents
        self.finished_rents = 0

        # Load data from files into attributes
        self.users = users
        self.bikes = {k:v for (k,v) in bikes.items() if v["Status"] == 10}
        self.bikes_battery = {k:v for (k,v) in bikes.items() if v["Status"] == 30}
        self.bikes_maintenance = {k:v for (k,v) in bikes.items() if v["Status"] == 40}
        self.total_bikes = len(bikes)
        self.total_users = len(users)
        self.active_users = 0
        self.geofences = {}
        self.geofences["lund"] = {k:v for (k,v) in geofences.items() if v["City"] == "lund"}
        self.geofences["karlskrona"] = {k:v for (k,v) in geofences.items() if v["City"] == "karlskrona"}
        self.geofences["stockholm"] = {k:v for (k,v) in geofences.items() if v["City"] == "stockholm"}

        # Create empty lists to house active and idle bikes
        self.active_bikes = []
        self.idle_bikes = []

        # Create the bike handlers and assign the routes to each them
        for k, v in self.bikes.items():

            # Take the data of each bike to create a bikehandler, match the bike id with route id to decode correct route
            self.idle_bikes.append(BikeHandler(v["id"], v["Position"], v["Speed"], v["Battery"], v["Status"], polyline.decode(routes[k]), self.geofences[v["City"]], udphost))

    def get_bike_index(self, type, id):
        """
        Get index for bike in active or idle list by id
        """
        # Define the needle
        needle = id

        # Define the haystack
        haystack = self.idle_bikes

        # Switch haystack if needed
        if type == "active":
            haystack = self.active_bikes

        # Iterate through the items in list to find a match
        for i, hs in enumerate(haystack):

            # If matched, return the index
            if int(hs.id) == int(needle):
                return i
        
        # If no key found
        return None

    def activate_from_app(self, bike, user, route):
        """
        Simulate a trip from the application with a specific bike and destination
        """
        # Find the bike list index
        ix = self.get_bike_index("idle", bike)

        if ix:
            # Add the selected route
            self.idle_bikes[ix].chapters = polyline.decode(route)

            # Create and register a rent in the database
            self.http.create_rent(user, bike)

            # Set the user to active
            self.users[str(user)] = 1

            # Assign the user to the bike object
            self.idle_bikes[ix].set_user(user)

            # Change the bike speed'
            self.idle_bikes[ix].set_speed(18)

            # Change the bike status to 'active'
            self.idle_bikes[ix].change_status(20)

            # Move the bike from 'idle' to 'active' in the simulation
            self.active_bikes.append(self.idle_bikes.pop(ix))

    def activate_bike(self, bikeId, i):
        """
        Activate bikes by triggering a trip
        """
        # Declare a variable for the user id
        userId = ""

        # To find the first available user we iterate through all users
        for user,active in self.users.items():

            # If the user attribute 'active' is False, proceed
            if not active:

                # Assign our user id variable with the selected users id
                userId = user
                self.active_users += 1

                # Break the loop
                break

        # Create and register a rent in the database
        self.http.create_rent(userId,bikeId)

        # Set the user to active
        self.users[str(userId)] = 1

        # Assign the user to the bike object
        self.idle_bikes[i].set_user(userId)

        # Change the bike status to 'active'
        self.idle_bikes[i].change_status(20)

        # Change the bike speed'
        self.idle_bikes[i].set_speed(18)

        # Move the bike from 'idle' to 'active' in the simulation
        self.active_bikes.append(self.idle_bikes.pop(i))


    def deactivate_bike(self, i, status):
        """
        Deactivate a bike by ending a trip
        """
        # Fetch the user
        user = self.active_bikes[i].get_user()

        # Register that the rent has ended in the database
        self.http.end_rent(user)

        # Change the bike status to desired code
        self.active_bikes[i].change_status(status)

        # Change the bike speed to 0
        self.active_bikes[i].set_speed(0)

        # Emit the data to let the database know that bike is available
        self.active_bikes[i].bike.emit_data()

        # Move the bike from 'active' to 'idle' in the simulation
        if status == 10:
            self.idle_bikes.append(self.active_bikes.pop(i))
        elif status == 30:
            self.active_bikes.pop(i)

        self.users[f"{user}"] = 0

        self.active_users -= 1

        # Increment the counter of finished rents
        self.finished_rents += 1
        

    def iterate_activation(self):
        """
        Iterate through all idle bikes with a chance to trigger activation
        """
        # Iterate through all idle bikes
        for i, bike in enumerate(self.idle_bikes):

            # If bike status is 'available' and the requirement of activation is achieved, proceed
            if bike.bike.get_status() == 10 and random.random() < self.activation_chance and len(bike.chapters) > 25:

                # Pass the bike to the 'activate' function
                self.activate_bike(bike.get_id(), i)

    def iterate_active(self):
        """
        Iterate through active bikes, make them emit data
        """
        # Iterate through all active bikes
        for i, bike in enumerate(self.active_bikes):

            # Make bike take the next step in simulation
            answer = bike.read_chapter()

            # A reply means the trip is finished
            if answer:

                # Pass the bike to the 'deactivate' function
                self.deactivate_bike(i, answer)

            # Sleep function to avoid sending all messages to bike server simultaneously
            time.sleep(0.00001)

    def iterate_idle(self):
        """
        Iterate through active bikes, make them emit data
        """
        # Iterate through all idle bikes
        for bike in self.active_bikes:

            # Make bike emit data to bike server
            bike.emit_data()

            # Sleep function to avoid sending all messages to bike server simultaneously
            time.sleep(0.00001)

    def deactivate_all(self):
        """
        Deactivate all active bikes
        """
        print("Deactivating all bikes")

        while self.active_bikes:
            for i, bike in enumerate(self.active_bikes):
                self.deactivate_bike(i, 10)
                time.sleep(0.001)
        
        self.read_active = True
        self.start()


    def start(self):
        """
        Start the simulation with looping actions
        """
        # This loop calls the 'iterate' functions every 'emit_frequency' seconds
        while True:
            tic1 = time.perf_counter() # Timer start

            if self.activation:
                self.iterate_activation()  # Idle bikes

            if self.read_active:
                self.iterate_active()      # Active bikes

                toc2 = time.perf_counter() # Timer stop

                if toc2 - tic1 > 5:
                    self.deactivate_all()
                    print(f"\n\nTotal time of the iteration was {toc2 - tic1} and exceded you emit frequency of {self.emit_frequency}")
                    print(f"Consider lowering the 'activation_chance' or raise the 'emit_frequency'.")
                    print("\nShutting down simulation safely..")
                    
                    break

                time.sleep(self.emit_frequency - (toc2 - tic1))

            else:
                self.deactivate_all()
