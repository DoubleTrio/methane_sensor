from dotenv import load_dotenv
from arcgis.gis import GIS
from arcgis import geometry 
import os
import time

print("starting script.")

load_dotenv()
password = os.environ.get("ARC_GIS_PASSWORD")

lat = 40.5509
long = -75.9738

gis = GIS("https://hamburg.maps.arcgis.com", "kacey.la", password)
wx_layer_search = gis.content.search(query='id: 7fba03cf4bc949cbbd8b7f046a0bde15')

wx_layer_coll_item = wx_layer_search[0]
wx_layers = wx_layer_coll_item.layers
wx_layer = wx_layers[0]
wx_fset = wx_layer.query()

input_geometry = {
    'y': float(lat),
    'x': float(long)
}

output_geometry = geometry.project(
    geometries = [input_geometry], 
    in_sr = 4326, 
    out_sr = wx_fset.spatial_reference['latestWkid'],
    gis = gis
)

print(output_geometry[0])

# Output layers in object
for field in wx_layer.properties['fields']:
    print(field['name'])

# Configure date - using UTC
dt=time.gmtime()  # Pulls UTC time from the pi
time_string = time.strftime("%m/%d/%Y, %H:%M:%S", dt)  # Formats the time to send to ArcGIS


# Create point object for insertion into map
wx_dict = {
    "attributes": { 
        "lat": lat,
        "long": long,
        "date": time_string,
        "ppm": 20,
    }, 
    "geometry": output_geometry[0]
}

add_result = wx_layer.edit_features(adds = [wx_dict])
print("complete.")
