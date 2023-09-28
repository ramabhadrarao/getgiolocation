import streamlit as st
import geocoder
import math
import networkx as nx
import matplotlib.pyplot as plt
import mysql.connector
from geopy.geocoders import Nominatim

# Connect to MySQL
mydb = mysql.connector.connect(**st.secrets["mysql"])

# Create a cursor object
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS giopositions (id INT AUTO_INCREMENT PRIMARY KEY, latitude DECIMAL(9,6), longitude DECIMAL(9,6))")

# Streamlit app
st.title("Get Location Coordinates")
geolocator = Nominatim(user_agent="my_geo_app")

# Function to get coordinates
def get_coordinates():
    try:
        location = geolocator.geocode("me", timeout=10)
        return location.latitude, location.longitude
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None, None

# Function to calculate haversine distance
def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # Radius of the Earth in kilometers
    R = 6371.0

    # Calculate the distance
    distance = R * c

    return distance

# Button to trigger location retrieval
button_clicked = st.button("Get Location")

if button_clicked:
    latitude, longitude = get_coordinates()
    st.write(f"Latitude: {latitude}")
    st.write(f"Longitude: {longitude}")

    # Store the coordinates in the MySQL table
    sql = "INSERT INTO giopositions (latitude, longitude) VALUES (%s, %s)"
    val = (latitude, longitude)
    mycursor.execute(sql, val)
    mydb.commit()
    st.write("Coordinates saved to MySQL database")


# Read coordinates from MySQL
coordinates = []
mycursor.execute("SELECT latitude, longitude FROM giopositions")

for record in mycursor.fetchall():
    coordinates.append((float(record[0]), float(record[1])))

#st.write(coordinates)
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
