import streamlit as st
import pandas as pd

# --- Function to load and prepare data ---
@st.cache_data
def load_data(nrows):
    data = pd.read_csv('directory 1.csv', nrows=nrows)
    # Normalize column headers
    data.columns = [str(c).strip().lower().replace(' ', '_') for c in data.columns]
    return data

# --- Country code to full name mapping ---
country_names = {
    'AD': 'Andorra',
    'AE': 'United Arab Emirates',
    'US': 'United States',
    'GB': 'United Kingdom',
    'CA': 'Canada',
    'FR': 'France',
    'DE': 'Germany',
    'CN': 'China',
    'JP': 'Japan',
    'IN': 'India',
    'SA': 'Saudi Arabia',
    'KW': 'Kuwait',
    'QA': 'Qatar',
    'OM': 'Oman',
    'BH': 'Bahrain',
    'SG': 'Singapore',
    'MY': 'Malaysia',
    'TH': 'Thailand',
    # Add more as needed
}

# --- Function to clean coordinates ---
def clean_coords(df):
    df = df.copy()
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df = df.dropna(subset=['latitude', 'longitude'])
    return df

# --- Load data ---
data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text('Done! (Using st.cache_data)')

# --- Add full country name column ---
if 'country' in data.columns:
    data['country_full_name'] = data['country'].map(country_names).fillna('Unknown')

# --- Show raw data ---
st.subheader('Raw Data')
st.dataframe(data)

# --- Global map of all Starbucks stores ---
if {'latitude', 'longitude'}.issubset(data.columns):
    st.subheader('🌍 Map of All Starbucks Stores')
    clean_data = clean_coords(data)
    st.map(clean_data[['latitude', 'longitude']])
else:
    st.warning("No latitude/longitude columns found, cannot plot map.")

# --- Bar chart: Number of stores per country ---
if 'country' in data.columns:
    st.subheader('📊 Number of Starbucks Stores per Country')

    # Count number of stores per country
    country_counts = data.groupby(['country', 'country_full_name']).size().reset_index(name='store_count')

    # Display table
    st.dataframe(country_counts)

    # Bar chart visualization
    st.bar_chart(country_counts.set_index('country')['store_count'])
else:
    st.error("The dataset doesn't have a 'Country' column. Please check your CSV file.")

# --- City filter for detailed view ---
if 'city' in data.columns:
    st.subheader('🏙️ Find Starbucks Stores by City')

    # Dropdown for city selection
    city_options = sorted(data['city'].dropna().unique())
    selected_city = st.selectbox('Select a City:', city_options)

    # Filter data for selected city
    filtered_data = data[data['city'] == selected_city]

    st.write(f"### Showing Starbucks stores in **{selected_city}**")
    st.dataframe(filtered_data)

    # --- Map view for selected city ---
    if {'latitude', 'longitude'}.issubset(filtered_data.columns):
        st.subheader(f"🗺️ Map of Starbucks Stores in {selected_city}")
        clean_filtered = clean_coords(filtered_data)
        st.map(clean_filtered[['latitude', 'longitude']])
