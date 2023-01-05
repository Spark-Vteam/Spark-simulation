"""
Setup for simulation, fetches data and generates routes
"""
import polyline
from src.helpers.http import Http
from src.helpers.routing import generate_route
import os
routes = {}


http = Http("http://localhost:4000/")

def get_users():
    """
    Fetch users from server and save them to file
    """
    # Open file in 'write' mode, specify output file and location
    with open('src/data/users.py', 'w') as fh:

        # Fetch users from server
        users = http.get("user")

        # Define separator to split each line
        separator = ",\n"

        # Write dictionary declaration
        fh.write("users = {\n")

        # Iterate through every user
        for  i, user in enumerate(users, start=1):

            # Check if its the last iteration, change separator if true
            if i == len(users):
                separator = "\n"

            # Format the data to dictionary
            # key = user id
            # value = boolean if user in rent, default to false
            fh.write(f'\t"{str(user["id"])}": 0{separator}')
        
        # Write dictionary ending syntax
        fh.write("}\n")

def get_bikes():
    """
    Fetch bikes from server and save them to file
    """
    # Open file in 'write' mode, specify output file and location
    with open('src/data/bikes.py', 'w') as fh:

        # Fetch bikes from server
        bikes = http.get("bike")

        # Define separator to split each line
        separator = ",\n"

        # Write dictionary declaration
        fh.write("bikes = {\n")

        # Iterate through every bike
        for  i, bike in enumerate(bikes, start=1):

            # Check if its the last iteration, change separator if true
            if i == len(bikes):
                separator = "\n"

            # Write dictionary declaration for the bike object
            fh.write(f'\t"{str(bike["id"])}": {"{"}\n')

            # Format all existing data to dictionary
            fh.write(f'\t\t"id": {bike["id"]},\n')
            fh.write(f'\t\t"User": 0,\n')
            fh.write(f'\t\t"Position": "{bike["Position"]}",\n')
            fh.write(f'\t\t"Battery": {bike["Battery"]},\n')
            fh.write(f'\t\t"Status": {bike["Status"]},\n')
            fh.write(f'\t\t"Speed": {bike["Speed"]},\n')
            fh.write(f'\t\t"City": "{bike["City"]}",\n')

            # Create additional data, only relevant to simulation
            fh.write(f'\t\t"Chapters": [],\n')

            # Write dictionary ending syntax for the bike object
            fh.write(f'\t\t{"}"}{separator}')
        
        # Write dictionary ending syntax
        fh.write("}\n")

def get_routes():
    """
    Generate routes based on bikes positions with randomized destinations
    """
     # Open file in 'write' mode, specify output file and location
    with open('src/data/routes.py', 'w') as fh:

        # Fetch bikes
        bikes = http.get("bike")

        # Define separator to split each line
        separator = ",\n"

        # Write dictionary declaration
        fh.write("routes = {\n")
        
        # Iterate through each bike
        for i, bike in enumerate(bikes):

            # Generate the route
            route = generate_route(bike["Position"])

            # Check if its the last iteration, change separator if true
            if i == len(bikes):
                separator = "\n"

            # Write list declaration for the route
            fh.write(f'\t"{str(bike["id"])}": [\n')

            # Iterate through positions in route
            for r in route:

                # Write the positions to the list
                fh.write(f'\t\t{r},\n')

            # Write list ending syntax for the route
            fh.write(f'\t\t]{separator}')

            os.system('clear')
            print(f"Generated {i} / {len(bikes)}")
        
        # Write dictionary ending syntax
        fh.write("}\n")

def encode_routes():
    """
    Encode an array of routes into polyline
    """
    separator = ",\n"
    # Open file in 'write' mode, specify output file and location
    with open('src/data/routes_encoded.py', 'w') as fh:

        fh.write('routes = {\n')

        for k,v in routes.items():
            try:
                fh.write(f'\t"{k}": "{polyline.encode(v)}"{separator}')
            except ValueError:
                print(k, v)

        fh.write('}')

def get_geofences():
    """
    Get and encode geofences from database
    """
    # Define the line separator
    separator = ",\n"

    # Fetch geofences from database
    geofences = http.get("geofence")

    # Open file in 'write' mode, specify output file and location
    with open('src/data/geofences.py', 'w') as fh:

        # Define the dictionary
        fh.write('geofences = {\n')

        for g in geofences:
            # Write dictionary declaration for the geofence object
            fh.write(f'\t"{str(g["id"])}": {"{"}\n')

            # Format all existing data to dictionary
            fh.write(f'\t\t"id": {g["id"]}{separator}')
            fh.write(f'\t\t"Coordinates": {g["Coordinates"]}{separator}')
            fh.write(f'\t\t"Info": "{g["Info"]}"{separator}')
            fh.write(f'\t\t"City": "{g["City"]}"{separator}')
            fh.write(f'\t\t"Type": {g["Type"]}\n')
            fh.write('\t\t}' + separator)

        # Close the dictionary
        fh.write('}')
