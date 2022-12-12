"""
Generating a trip
"""
import requests
import json
import random
import polyline

def generate_coordinates(position):
        """
        Calculate destination from current position
        """
        radius = 0.02 # In degrees, 0.02 is roughly 2.2KM
        position = position.split(",") # Extract the positions
        destination_lat = random.uniform(float(position[0])-radius,float(position[0])+radius) # Calculate destination latitude based on radius from "radius" variable
        destination_lon = random.uniform(float(position[1])-radius,float(position[1])+radius) # Calculate destination longitude based on radius from "radius" variable

        return [(position[0],position[1]),(destination_lat,destination_lon)]

def plot_route(start, destination):
    """
    Get a list of coordinates that makes a trip
    """
    route_url=f'http://router.project-osrm.org/route/v1/biking/{start[1].strip()},{start[0]};{destination[1]},{destination[0]}?alternatives=true&geometries=polyline'
    r=requests.get(route_url)
    res=r.json()
    return polyline.decode(res["routes"][0]["geometry"])


def standard_trip(position):
    """
    
    """
    positions = generate_coordinates(position)

    route = plot_route(positions[0], positions[1])
    # print(route)
    return route

    # return plot_route(positions[0], positions[1])


    