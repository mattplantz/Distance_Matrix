import pandas as pd
import streamlit as st
import json
import requests

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


st.title("Distance Matrix Generator")

if 'locs' in st.session_state:
   locs = st.session_state.locs
else:
   st.write("Please ensure the file you upload has the following headers: ID | latitude | longitude")
   uploaded_file = st.file_uploader(label = "Please upload transfer data here", type = ['xlsx'], accept_multiple_files= False)
   if uploaded_file:
       st.success("Upload Successful")
       locs = pd.read_excel(uploaded_file)
       locs = locs.set_index('ID')


@st.cache_data
def create_dist_matrix(locs: pd.DataFrame):
    dist = pd.DataFrame(index=locs.index,
                                  columns=locs.index)
    for orig, orig_loc in locs.iterrows():
        print(orig)
        for dest, dest_loc in locs.iterrows():
            lat_1 = orig_loc.at['latitude']
            lon_1 = orig_loc.at['longitude']
            lat_2 = dest_loc.at['latitude']
            lon_2 = dest_loc.at['longitude']
            r = requests.get(
                f"http://router.project-osrm.org/route/v1/car/{lon_1},{lat_1};{lon_2},{lat_2}?overview=false""")
            # then you load the response using the json libray
            routes = json.loads(r.content)
            route_1 = routes.get("routes")[0]['distance']
            # output is in meters so divide by 1609 to get to miles
            route_1 = route_1 / 1609.344
           # print(route_1)
            dist.at[orig, dest] = route_1
    return dist

if uploaded_file or 'locs' in st.session_state:
    dist = create_dist_matrix(locs)
    dist = dist.astype(float)
    st.dataframe(dist)
    csv = convert_df(dist)
    st.download_button(
           "Press to Download",
           csv,
           "lat_lon_output.csv",
           "text/csv",
           key='download-csv'
        )
