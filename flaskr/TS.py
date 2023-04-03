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
    
    if driving != []:
        #get driving time
        driving_time = driving[0]["legs"][0]["duration"]["text"] if driving != [] else None  #return a string
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
            
         #get driving distance
        driving_distance = driving[0]["legs"][0]["distance"]["text"] if driving != [] else None  #return a string
        distance_value, distance_unit = driving_distance.split(" ")
        if distance_unit == 'mi': #eg 2,612 mi
            distance_value = float(distance_value.replace(",", ""))
        if distance_unit != 'mi': # ft or fts
            distance_value = float(distance_value.replace(",", ""))/5280  #convert to mile
             
    if driving == []:
        walking = gmaps.directions(a_position, b_position, mode="walking", departure_time=now)
        walking_time = walking[0]["legs"][0]["duration"]["text"] if walking != [] else None  #return a string
        walking_time_split = walking_time.split(" ")
        if len(walking_time_split) == 2:  # eg 34 mins or 2 hours
            time_value = walking_time_split[0]
            time_unit = walking_time_split[1]
            if time_unit  == 'min' or 'mins':
                time_value = float(time_value)/60
            if time_unit  == 'hour' or 'hours':
                time_value = float(time_value)
        if len(walking_time_split) == 4:  # eg 1 hour 4 mins
            time_value_hr = walking_time_split[0]
            time_value_min = walking_time_split[2]
            time_value = float(time_value_hr) + float(time_value_min)/60
        
        walking_distance = walking[0]["legs"][0]["distance"]["text"] if walking != [] else None  #return a string
        distance_value, distance_unit = walking_distance.split(" ")
        if distance_unit == 'mi':
            distance_value = float(distance_value.replace(",", ""))
        if distance_unit != 'mi': # ft or fts
            distance_value = float(distance_value.replace(",", ""))/5280
    
    return (time_value, distance_value)


def tsp(loca):
    start = datetime.now()
    shortest_path = None
    route_distance = shortest_time = float('inf')
    pair_time_all = {}   # save all the possible 2 POI combinations travel time
    pair_time_route = {}  # only save travel time of possible 2 POI combinations from shortest path
 
    for path in itertools.permutations(loca['thing_title']):
        total_distance = 0
        total_time = 0
        for i in range(len(path) - 1):
            a_position = [float(loca[loca['thing_title'] == path[i]]['lat']), float(loca[loca['thing_title'] == path[i]]['lon'])]
            b_position = [float(loca[loca['thing_title'] == path[i+1]]['lat']), float(loca[loca['thing_title'] == path[i+1]]['lon'])]
            direction = distance(a_position, b_position)
            pair_time_all[(path[i],path[i+1])] = direction[0]
            total_time += direction[0]
            total_distance += direction[1]
        if total_time < shortest_time:
            shortest_time = total_time
            route_distance = total_distance
            shortest_path = path
      
    for i in range(len(shortest_path)-1):
        if (shortest_path[i], shortest_path[i+1]) in pair_time_all.keys():
            pair_time_route[(shortest_path[i], shortest_path[i+1])] = pair_time_all[(shortest_path[i], shortest_path[i+1])]
                    
    end = datetime.now()
    cal_time = end - start
    return shortest_path, shortest_time, route_distance, pair_time_route, cal_time

#Example1 acad park
# A = {"thing_title": "Hike Double Bubble Nubble Loop with Island Explorer", "lat":44.350011499069, 'lon':-68.2414535993951}
# B = {"thing_title": "Hike Great Head Trail", "lat": 44.3300018310546, 'lon':-68.1775283813476}
# C = {"thing_title": "Hike Ship Harbor Trail", "lat": 44.2284927368164, 'lon':-68.3237609863281}
# D = {"thing_title": "Hike Giant Slide Loop", "lat": 44.35079167, 'lon':-68.30218833}
# E = {"thing_title": "Hike Gorge Path", "lat": 44.372621, 'lon':-68.221942}
# loca = pd.DataFrame([A,B,C,D])

#Example2 yell park
# A = {"thing_title": "Natural Bridge Trail", "lat":40.754898, 'lon':-122.323452}
# B = {"thing_title":"Ribbon Lake Trail", "lat": 44.719745, 'lon':-110.485320}
# C = {"thing_title": "Beaver Ponds Trail", "lat": 44.967939, 'lon':-110.704438}
# loca = pd.DataFrame([A,B,C])

# shortest_path, shortest_time, shortest_distance, pair_time_route, cal_time = tsp(loca)
# print("Shortest path:", shortest_path)
# print("Shortest time in hour :", shortest_time)
# print("Route distance in mile:", shortest_distance)
# print("Pairs time:", pair_time_route)
# print("Calculation time:", cal_time)