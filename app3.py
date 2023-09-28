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

# Function to get coordinates
def get_coordinates():
    try:
        location = geolocator.geocode("me", timeout=10)
        return location.latitude, location.longitude
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None, None


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
for record in mycursor.fetchall():
    coordinates.append((float(record[1]), float(record[2])))

# Calculate distances and create network diagram
G = nx.Graph()
for i, (lat1, lon1) in enumerate(coordinates):
    G.add_node(i, pos=(lat1, lon1))
    for j, (lat2, lon2) in enumerate(coordinates):
        if i != j:
            distance = math.dist((lat1, lon1), (lat2, lon2))
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
