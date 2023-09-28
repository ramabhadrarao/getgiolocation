import streamlit as st

# Streamlit app
st.title("Get Location Coordinates")

# Add a button that will trigger the geolocation feature
button_clicked = st.button("Get Location")

# Add a placeholder for the result
result = st.empty()

if button_clicked:
    # Use JavaScript to get the user's location
    js_code = """
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition);
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    }

    function showPosition(position) {
        var latitude = position.coords.latitude;
        var longitude = position.coords.longitude;
        var result = "Latitude: " + latitude + "<br>Longitude: " + longitude;
        document.getElementById("result").innerHTML = result;
    }
    </script>
    <button onclick="getLocation()">Get Location</button>
    <div id="result"></div>
    """

    # Display the HTML and JavaScript code
    result.markdown(js_code, unsafe_allow_html=True)
