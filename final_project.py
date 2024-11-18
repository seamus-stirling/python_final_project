import pandas as pd
import pydeck as pdk
import streamlit as st
import numpy as np
from altair import layer


# Takes the raw data that I downloaded and reorganized and puts it into a dataframe only using the important info columns
def read_data(csv_file):
    restaurant_data = pd.read_csv(csv_file, usecols=[1,2,3,4,5,6,7,8,9], index_col="name")
    return restaurant_data

# Using the restaurant data and my city list I read all of the data for the corresponding city into a dictionary
def city_splitter(restaurant_data):
    cities = ["Boston", "New York", "Los Angeles", "Philadelphia", "Atlanta"]
    city_restaurant_data = {city: restaurant_data[restaurant_data['city'] == city] for city in cities}
    return city_restaurant_data, cities

def city_maps(city_restaurant_data, city_selector):
    st.write("Current City:", city_selector)
    selected_city = city_selector
    view_state = pdk.ViewState(
        latitude = float(city_restaurant_data[selected_city]["latitude"].mean()),
        longitude = float(city_restaurant_data[selected_city]["longitude"].mean()),
        zoom = 11,
        pitch = 0
    )
    layer = [
        pdk.Layer(
            "ScatterplotLayer",
            data = city_restaurant_data[selected_city],
            get_position = ["longitude", "latitude"],
            get_color = "[255, 0, 0]",
            get_radius = 100,
            )
    ]
    map = pdk.Deck(
        map_style ="mapbox://styles/mapbox/light-v9",
        initial_view_state = view_state,
        layers = layer
    )
    st.pydeck_chart(map)
    return

def city_dataframe(city_restaurant_data, city_selector):
    st.dataframe(
        city_restaurant_data[city_selector],
        column_config={
            "categories": "Restaurant Type",
            "name": "Name",
            "address": "Street",
            "city": "City",
            "province": "State",
            "postalCode": "Zip Code",
            "latitude":"Latitude",
            "longitude": "Longitude"
        }
    )

def home_page(city_restaurant_data, cities):
    #st.header("Fast Food Restaurants by City")
    st.title("Fast Food Restaurants by City")
    city_selector = st.selectbox("Select a City", cities)
    column1, column2 = st.columns(2)
    with column1:
        st.header = "Interactive Map"
        city_maps(city_restaurant_data, city_selector)
    with column2:
        st.header = "Restaurant Locations"
        city_dataframe(city_restaurant_data, city_selector)


def most_locations():

    return

def popularity_map():

    return

def logo():

    return

def main():
    csv_file = "fast_food_usa.csv"
    restaurant_data = read_data(csv_file)
    city_restaurant_data, cities = city_splitter(restaurant_data)
    home_page(city_restaurant_data, cities)
main()