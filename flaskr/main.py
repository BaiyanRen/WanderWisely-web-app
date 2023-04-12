from flask import Flask, render_template, request
import pandas as pd
from flaskr import helper_functions as uf
from flaskr import get_park as gp
from flaskr.TS import tsp
from math import ceil



# build database connection

conn, engine = uf.conn_to_db()

# get Activities and Amenities
activities = uf.import_data("select * from wanderwisely.things_to_do_places", conn)
activities = activities["activity_name"].unique()
amenities = uf.import_data("select * from wanderwisely.amenity_related_parks", conn)
amenities = amenities["name"].unique()
# load data to map parkCode to parkName
parks_df = uf.import_data(f"select * from wanderwisely.activity_related_parks", conn)

# record user's selection
user_selection = {"activities": [], "amenities": [], "pois": [],"hours":[], "park":[]}

def update_selection(selection, select_type):
    if select_type == "hours" or select_type == "park":
            user_selection[select_type] = [selection]
    else: # when select_type == amenities, activities, pois
        if selection in user_selection[select_type]:
            user_selection[select_type].remove(selection)
        else:
            user_selection[select_type].append(selection)

def initiate_selection():
    user_selection["activities"] = []
    user_selection["amenities"] = []
    user_selection["pois"] = []
    user_selection["hours"] = []
    user_selection["park"] = []

app = Flask(__name__)

@app.route('/')
def home():
    initiate_selection()
    return render_template('home.html')


@app.route('/ActivitiesAndAmenities')
def ActivitiesAndAmenities():
    initiate_selection()
    return render_template('ActivitiesAndAmenities.html', activities=activities, amenities=amenities)


@app.route('/record_button', methods=['POST'])
def record_button():
    data = request.get_json()
    update_selection(data["input"], data["type"])
    # Record the button click in the database or perform any other action
    print(user_selection)
    return '', 204


@app.route('/parks')
def parks():
    # initiate parks in case users come back to the page
    user_selection["park"] = []
    amenity_names=user_selection['amenities']
    activity_names=user_selection['activities']
    top_three_parks = gp.get_park(amenity_names,activity_names)
    hours = [1,2,3,4,5,6,7,8,9,10,11,12]
    return render_template('parks.html',parks = top_three_parks, hours = hours)


def generate_places(parkName, activities):
    parkCode = parks_df[parks_df['parkName'] == parkName]['parkCode'].tolist()[0]
    activities = "','".join(activities)
    query = f"select thing_title from wanderwisely.things_to_do_places where parkCode = '{parkCode}' and activity_name in ('{activities}')"
    places_df = uf.import_data(query, conn)
    filtered_places = places_df['thing_title'].to_list()
    return filtered_places


@app.route('/poi')
def poi():
    # initiate pois in case users come back to the page
    user_selection["pois"] = []
    parkName = user_selection['park'][0]
    activities = user_selection['activities']
    places = generate_places(parkName, activities)
    
    return render_template('poi.html', parkName=parkName, places=places)


# get lat/lon of selected places
@app.route('/generate_route')
def generate_route():
    conn, engine = uf.conn_to_db()
    query = """select distinct thing_title, lat, lon, duration from wanderwisely.things_to_do_places as table1
    inner join wanderwisely.activity_related_parks as table2
    on table1.parkCode = table2.parkCode
    where parkName = '{}' AND thing_title in {} """ .format(*user_selection['park'], tuple(user_selection['pois']))
    loca = uf.import_data(query, conn)

    # A = {"thing_title": "Hike Double Bubble Nubble Loop with Island Explorer", "lat":44.350011499069, 'lon':-68.2414535993951, "duration": 2.0}
    # B = {"thing_title": "Hike Great Head Trail", "lat": 44.3300018310546, 'lon':-68.1775283813476, "duration": 4.0}
    # C = {"thing_title": "Hike Ship Harbor Trail", "lat": 44.2284927368164, 'lon':-68.3237609863281, "duration": 1.0}
    # D = {"thing_title": "Hike Giant Slide Loop", "lat": 44.35079167, 'lon':-68.30218833, "duration": 4.0}
    # E = {"thing_title": "Hike Gorge Path", "lat": 44.372621, 'lon':-68.221942, "duration": 3.0}
    # F = {"thing_title": "Hike Wonderland Trail", "lat": 44.23383331298821, 'lon':-68.3199996948242, "duration": 0.5}
    # G = {"thing_title": "Hike Beachcroft Path", "lat": 44.3585023529493, 'lon':-68.2059851525353, "duration": 1.5}
    # loca = pd.DataFrame([A,B,C,D,E,F,G])

    print(loca)
    #get route
    locations, location_names, route_order, shortest_time, route_pair_distance, route_pair_time, duration, cal_time = tsp(loca)
    total_time = round(shortest_time + sum(loca['duration']), 2)

    # load images for places
    route_order_sql = "','".join(route_order)
    query = f"select thing_title, image_url, place_url from wanderwisely.things_to_do_places where thing_title in ('{route_order_sql}')"
    route_data = uf.import_data(query, conn)
    route_data_dict = route_data.set_index('thing_title').to_dict()
    days = ceil(total_time/float(user_selection["hours"][0]))

    print("dictionary of route data: ", route_data_dict)
    print("shortest_path: ", route_order)
    print("total: ", total_time)
    print("route_pair_distance: ", route_pair_distance)
    print("route_pair_time: ", route_pair_time)
    print("duration: ", duration)
    print("cal time: ", cal_time)
    print("locations type: ", type(locations))
    print("locations: ", locations)


    return render_template('generate_route.html', park = user_selection['park'][0], locations = locations, days = days, route_order = route_order,
                           total_time = total_time, route_pair_distance = route_pair_distance,
                           route_pair_time = route_pair_time, duration = duration, route_data_dict = route_data_dict)




@app.route('/contact')
def contact():
    return render_template('contact.html')




