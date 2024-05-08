import streamlit as st

st.title("Geocoding Automation")
st.markdown('''
  The goal of this application is to be a one-stop shop for calculating drive distances between a list of locations. The application contains two modules:
      - ** Latitude and Longitude Generator**: This module generates the latitude and longitude for a US address using the geopy package
      - ** Distance Matrix Generator**: This module creates a distance matrix for a given set of locations with latitude and longitude coordinates. It can either use output from the lat / lon module or use user uploaded data.
''')
