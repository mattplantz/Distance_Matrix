import streamlit as st
import pandas as pd
from geopy.geocoders import Photon
from geopy.extra.rate_limiter import RateLimiter

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

st.title('Latitude and Longitude Generator')
st.write('Please ensure the uploaded file only contains two columns named: ID and Address')

# set up for geocoding
locator = Photon(user_agent="measurements")
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

# user upload
uploaded_file = st.file_uploader(label = "Please upload address data here as an Excel file", type = ['xlsx'], accept_multiple_files= False)

if uploaded_file:
  st.success("Address Upload Successful")
  locs = pd.read_excel(uploaded_file)
  locs = locs.set_index('ID')
  locs['location'] = locs['Address'].apply(geocode)
  locs['point'] = locs['location'].apply(lambda loc: tuple(loc.point) if loc else None)
  locs[['latitude', 'longitude', 'altitude']] = pd.DataFrame(locs['point'].tolist(), index=locs.index)
  locs = locs[['latitude','longitude']]
  if 'locs' not in st.session_state:
      st.session_state.locs = locs
  locs = locs.reset_index()
  csv = convert_df(locs)
  st.download_button(
         "Click to Download Output",
         csv,
         "lat_lon_output.csv",
         "text/csv",
         key='download-csv'
      )
  st.dataframe(locs)
