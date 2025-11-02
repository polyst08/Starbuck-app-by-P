import streamlit as st      
import pandas as pd          
import numpy as np            
 
# Function to load CSV data
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
 
# Display the raw data
st.subheader('Raw Data')
st.write(data)