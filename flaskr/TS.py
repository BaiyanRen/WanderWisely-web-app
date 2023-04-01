import itertools
import pandas as pd

#calculate distance bwt 2 POI based on lat/long

def distance(POI_1, POI_2):
    return (float((POI_1["lat"]) - float(POI_2["lat"]))**2 + (float(POI_1["lon"]) - float(POI_2["lon"]))**2)**0.5

def tsp(loca):
    shortest_path = None
    shortest_distance = float('inf')
    for path in itertools.permutations(loca['thing_title']):
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += distance(loca[loca['thing_title'] == path[i]], loca[loca['thing_title'] == path[i+1]])
        if total_distance < shortest_distance:
            shortest_distance = total_distance
            shortest_path = path
    return shortest_path, shortest_distance

# Example
A = {"thing_title": "A", "lat": 2, 'lon':3}
B = {"thing_title": "B", "lat": 6, 'lon':2}
C = {"thing_title": "C", "lat": 2, 'lon':5}
loca = pd.DataFrame([A,B,C])

shortest_path, shortest_distance = tsp(loca)
print("Shortest path:", shortest_path)
print("Shortest distance:", shortest_distance)