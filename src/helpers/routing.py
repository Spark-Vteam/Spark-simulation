"""
Generating a trip
"""
import requests
import json
import random
import polyline
from geopy import distance, units

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

def points_between(a, b):
    """
    Get every x meters between two points
    """
    points_lat = []
    points_lon = []
    d = distance.distance(a, b).m
    if d > 5:
        d = int(d / 5)
        lat_dif = ((b[0] - a[0]) / d)
        lon_dif = ((b[1] - a[1]) / d)
        for i in range(0,d):
            points_lat.append(a[0] + (lat_dif * i))

        for i in range(0,d):
            points_lon.append(a[1] + (lon_dif * i))

        points = list(zip(points_lat, points_lon))
        return points
    return[a,b]


def fill_route(route):
    """
    Make route more precise
    """
    full_route = []
    for i in range(1,len(route)):
        full_route += (points_between(route[i-1], route[i]))
    return full_route


def generate_route(position, destination=None):
    """
    Generate a trip
    """
    if destination:
        pos_list = position.split(",")
        des_list = destination.split(",")
        positions = [(pos_list[0],pos_list[1]),(des_list[0],des_list[1])]
    else:
        positions = generate_coordinates(position)

    route = plot_route(positions[0], positions[1])
    
    route = fill_route(route)

    return polyline.encode(route)

    