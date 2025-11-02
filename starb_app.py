import streamlit as st      
import pandas as pd          
import numpy as np            
 
@st.cache_data
def load_data(nrows):
    data = pd.read_csv('directory 1.csv', nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data
 
# Display a loading message
data_load_state = st.text('Loading data...')
 
# Load 10,000 rows of data
data = load_data(10000)
 
# Notify that loading is complete
data_load_state.text('Done! (Using st.cache_data)')
 
# --- Dropdown to select city ---
if 'city' in data.columns:
    st.subheader('Find Starbucks Stores by City')

    # Clean up missing values and sort
    city_options = sorted(data['city'].dropna().unique())
    selected_city = st.selectbox('Select a City:', city_options)

    # Filter data based on selected city
    filtered_data = data[data['city'] == selected_city]

    st.write(f"### Showing Starbucks stores in **{selected_city}**")
    st.dataframe(filtered_data)

    # --- Optional: Map view if coordinates exist ---
    if {'latitude', 'longitude'}.issubset(filtered_data.columns):
        st.subheader("Map of Starbucks Stores")
        st.map(filtered_data[['latitude', 'longitude']])
else:
    st.error("The dataset doesn't have a 'City' column. Please check the CSV file.")

