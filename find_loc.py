import pandas as pd
import googlemaps

def get_state_from_coordinates(latitude, longitude):
    gmaps = googlemaps.Client(key="*INSERT_KEY_HERE*")
    try:
        result = gmaps.reverse_geocode((latitude, longitude))[0]
        state = None
        for component in result['address_components']:
            if 'administrative_area_level_1' in component['types']:
                state = component['long_name']
                break
        if state:
            return state
        else:
            return "State not found for the given coordinates"
    except Exception as e:
        print("Error:", e)
        return "Error occurred while fetching state for the given coordinates"

data = pd.read_csv("plumes_2017-01-01_2018-01-01.csv")

latitude = data.loc[0, 'plume_latitude']
longitude = data.loc[0, 'plume_longitude']

state = get_state_from_coordinates(latitude, longitude)

print("This dataset is from " + state)
