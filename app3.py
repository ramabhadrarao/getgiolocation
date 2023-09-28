import streamlit as st
import geocoder
import math
import networkx as nx
import matplotlib.pyplot as plt
import mysql.connector
from geopy.geocoders import Nominatim
from datetime import datetime

# Connect to MySQL
mydb = mysql.connector.connect(**st.secrets["mysql"])

# Create a cursor object
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS giopositions (id INT AUTO_INCREMENT PRIMARY KEY, latitude DECIMAL(9,6), longitude DECIMAL(9,6))")

# Streamlit app
st.title("Get Location Coordinates")
# Function to get coordinates
def get_coordinates():
    geolocator = Nominatim(user_agent="my_geo_app")  # Define geolocator here
    latitude = st.session_state['latitude']
    longitude = st.session_state['longitude']
    st.write(f"Latitude: {latitude}")
    st.write(f"Longitude: {longitude}")

# Trigger button to get location
if 'latitude' not in st.session_state:
    st.session_state['latitude'] = None

if 'longitude' not in st.session_state:
    st.session_state['longitude'] = None

if st.button("Get Location", key=datetime.now()):
    geolocator = Nominatim(user_agent="my_geo_app")  # Define geolocator here
    location = geolocator.geocode("me", timeout=10)
    if location:
        st.session_state['latitude'] = location.latitude
        st.session_state['longitude'] = location.longitude
    else:
        st.error("Error occurred while fetching coordinates. Please try again.")

get_coordinates()


# Read coordinates from MySQL
coordinates = []
mycursor.execute("SELECT latitude, longitude FROM giopositions")

for record in mycursor.fetchall():
    coordinates.append((float(record[0]), float(record[1])))

# Calculate distances and create network diagram
G = nx.Graph()
for i, (lat1, lon1) in enumerate(coordinates):
    G.add_node(i, pos=(lat1, lon1))
    for j, (lat2, lon2) in enumerate(coordinates):
        if i != j:
            distance = haversine(lat1, lon1, lat2, lon2)
            G.add_edge(i, j, weight=distance)

# Draw network diagram
fig, ax = plt.subplots()
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, pos, with_labels=True, ax=ax)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
st.pyplot(fig)

# Close MySQL connection
mycursor.close()
mydb.close()
