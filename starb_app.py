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
 
# --- Bar chart: Number of stores per country ---
if 'country' in data.columns:
    st.subheader('Number of Starbucks Stores per Country')

    # Count number of stores per country
    country_counts = data['country'].value_counts().reset_index()
    country_counts.columns = ['country', 'store_count']

    # Display data table
    st.dataframe(country_counts)

    # Display bar chart
    st.bar_chart(country_counts.set_index('country'))
else:
    st.error("The dataset doesn't have a 'Country' column. Please check your CSV file.")

# --- City filter for detailed view ---
if 'city' in data.columns:
    st.subheader('Find Starbucks Stores by City')

    # Dropdown for city selection
    city_options = sorted(data['city'].dropna().unique())
    selected_city = st.selectbox('Select a City:', city_options)

    # Filter data for the selected city
    filtered_data = data[data['city'] == selected_city]

    st.write(f"### Showing Starbucks stores in **{selected_city}**")
    st.dataframe(filtered_data)

    # --- Map view ---
    if {'latitude', 'longitude'}.issubset(filtered_data.columns):
        st.subheader("Map of Starbucks Stores in Selected City")
        st.map(filtered_data[['latitude', 'longitude']])

