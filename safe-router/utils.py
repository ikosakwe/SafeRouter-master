#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from simplification.cutil import simplify_coords
import requests
import os

MAPBOX_ACCESS_TOKEN = os.environ.get('MAPBOX_TOKEN')

# format coordinates to mapbox style
def format_coordinates(points):
    string_coordinates = ""
    N = len(points)
    for point in points:
        
        string_coordinates+= str(point[0])+ ","+ str(point[1])+";"
    
    return string_coordinates[:-1]

def get_mapbox_route(path):
    coordinates = format_coordinates(path)
    N = len(path)-1
    waypoints = "0;"+str(N)
    api = "https://api.mapbox.com/matching/v5/mapbox/driving/{}.json?overview=full&annotations=distance,duration,congestion&geometries=polyline6&waypoints={}&steps=true&banner_instructions=true&voice_instructions=true&voice_units=metric&tidy=true&access_token={}"
    req = api.format(coordinates,waypoints,MAPBOX_ACCESS_TOKEN)
    response = requests.get(req)
    return response.content

# simplify polyline to 100 points
def simplify_polyline(route):
    precision = 0.0001
    simplified = route

    while len(simplified)>100:
        
        simplified = simplify_coords(route, precision)
        precision = precision + 0.0005
    
    return simplified

