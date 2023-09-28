import streamlit as st
import geocoder

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
