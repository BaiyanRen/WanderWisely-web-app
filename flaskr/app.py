from flask import Flask, render_template, request
import pandas as pd
import helper_functions as uf
import get_park

# build database connection

conn, engine = uf.conn_to_db()

# get Activities and Amenities
activities = uf.import_data("select * from wanderwisely.activity_related_parks", conn)
activities = activities["name"].unique()
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

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/ActivitiesAndAmenities')
def ActivitiesAndAmenities():
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
    amenity_ids=user_selection['amenities']
    activity_ids=user_selection['amenities']
    top_three_parks = get_park(amenity_ids,activity_ids)
    hours = user_selection['hours']
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
    parkName = user_selection['park'][0]
    activities = user_selection['activities']
    places = generate_places(parkName, activities)
    # parkName = 'Yosemite National Park'
    # places = generate_places('Yosemite National Park', ['Hiking', 'Biking', 'Astronomy', 'Boating'])
    return render_template('poi.html', parkName=parkName, places=places)

# get lat/lon of selected places
tpl = ('Go Earthcaching At Acadia', 'Bike Carriage Roads')
query = """select thing_title, lat, lon from wanderwisely.things_to_do_places as table1
    inner join wanderwisely.activity_related_parks as table2
    on table1.parkCode = table2.parkCode
    where parkName = '{}' AND thing_title in {} """ .format('Acadia National Park', tpl)
loca = uf.import_data(query, conn)


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)


