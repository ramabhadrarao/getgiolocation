import streamlit as st
import geocoder

# Function to get coordinates
def get_coordinates(location_name):
    g = geocoder.osm(location_name)
    return g.lat, g.lng

# Streamlit app
st.title("Get Location Coordinates")

# Button to trigger location retrieval
if st.button("Get Location"):
    location_name = st.text_input("Enter location name:")
    if location_name:
        latitude, longitude = get_coordinates(location_name)
        st.write(f"Location Name: {location_name}")
        st.write(f"Latitude: {latitude}")
        st.write(f"Longitude: {longitude}")
    else:
        st.write("Please enter a location name.")
