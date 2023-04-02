import itertools
import pandas as pd
import googlemaps
from datetime import datetime

API_key = 'AIzaSyBHD-lOFZgRIJiSSyGzA51S5jFZ6b386NU'#enter Google Maps API key
gmaps = googlemaps.Client(key=API_key)

#calculate distance bwt 2 POI based on lat/long

def distance(a_position, b_position):
    now = datetime.now()
    driving = gmaps.directions(a_position, b_position, mode="driving", departure_time=now)
    driving_time = driving[0]["legs"][0]["duration"]["text"] if driving != [] else None
    driving_time_split = driving_time.split(" ")
    if len(driving_time_split) == 2:  # eg 34 mins or 2 hours
        time_value = driving_time_split[0]
        time_unit = driving_time_split[1]
        if time_unit  == 'min' or 'mins':
            time_value = float(time_value)/60
        if time_unit  == 'hour' or 'hours':
            time_value = float(time_value)
    if len(driving_time_split) == 4:  # eg 1 hour 4 mins
        time_value_hr = driving_time_split[0]
        time_value_min = driving_time_split[2]
        time_value = float(time_value_hr) + float(time_value_min)/60
        
    driving_distance = driving[0]["legs"][0]["distance"]["text"] if driving != [] else None
    distance_value, distance_unit = driving_distance.split(" ")
    if distance_unit == 'mi':
        distance_value = float(distance_value)
    if distance_unit != 'mi': # ft or fts
        distance_value = float(distance_value)/5280
    
    return (time_value, distance_value)


def tsp(loca):
    shortest_path = {}
    shortest_distance = shortest_time = float('inf')
    for path in itertools.permutations(loca['thing_title']):
        total_distance = 0
        total_time = 0
        for i in range(len(path) - 1):
            a_position = [float(loca[loca['thing_title'] == path[i]]['lat']), float(loca[loca['thing_title'] == path[i]]['lon'])]
            b_position = [float(loca[loca['thing_title'] == path[i+1]]['lat']), float(loca[loca['thing_title'] == path[i+1]]['lon'])]
            direction = distance(a_position, b_position)
            total_time += direction[0]
            total_distance += direction[1]
        if total_distance < shortest_distance:
            shortest_distance = total_distance
            shortest_time = total_time
            short_route = path
    for p in short_route:
        shortest_path[p] = [float(loca[loca['thing_title'] == p]['lat']), float(loca[loca['thing_title'] == p]['lon'])]
    return shortest_path, shortest_time, shortest_distance

#Example
# A = {"thing_title": "A", "lat":44.362291699252, 'lon':-68.2076065006421}
# B = {"thing_title": "B", "lat": 44.300245999522, 'lon':-68.3498804911828}
# C = {"thing_title": "C", "lat": 44.29906967, 'lon':-68.31566767}
# loca = pd.DataFrame([A,B,C])

# shortest_path, shortest_time, shortest_distance = tsp(loca)
# print("Shortest path:", shortest_path)
# print("Shortest time in hour :", shortest_time)
# print("Shortest distance in mile:", shortest_distance)