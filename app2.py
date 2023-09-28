import streamlit as st
import geocoder
import math
import csv
import networkx as nx
import matplotlib.pyplot as plt

# Streamlit app
st.title("Get Location Coordinates")

# Function to get coordinates
def get_coordinates():
    g = geocoder.ip('me')
    return g.lat, g.lng

# Button to trigger location retrieval
button_clicked = st.button("Get Location")

if button_clicked:
    latitude, longitude = get_coordinates()
    st.write(f"Latitude: {latitude}")
    st.write(f"Longitude: {longitude}")

    # Store the coordinates in a CSV file
    with open('location_coordinates.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Latitude', 'Longitude'])
        writer.writerow([latitude, longitude])
        st.write("Coordinates saved to location_coordinates.csv")

# Read coordinates from CSV
coordinates = []
with open('location_coordinates.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        coordinates.append((float(row['Latitude']), float(row['Longitude'])))

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
