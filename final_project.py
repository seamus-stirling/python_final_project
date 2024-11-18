"""
Name:       Seamus Stirling
CS230:      Section 6
Data:       Fast Food Restaurants in the USA
URL:
Description:

This program takes a data file full of fast food locations in the United States and offers and interactive way to visualize the data.
"""


import pandas as pd
import pydeck as pdk
import streamlit as st
import numpy as np
from altair import layer


# [PY3], [DA1], [DA9] Takes the raw data that I downloaded and reorganized and puts it into a dataframe only using the important info columns
def read_data(csv_file):
    try:
        restaurant_data = pd.read_csv(csv_file, usecols=[1,2,3,4,5,6,7,8,9], index_col="name")
        restaurant_data["Full Address"] = restaurant_data.apply(lambda row: f"{row['address']}, {row['city']}, {row['province']}", axis=1)
        return restaurant_data
    except Exception as e:
        st.error("Error: The file is either empty, unreadable, or missing a column")

# [PY2], [PY4], [PY5], and [DA5] Using the restaurant data and my city list I read all of the data for the corresponding city into a dictionary
def city_splitter(restaurant_data):
    cities = ["Boston", "New York", "Los Angeles", "Philadelphia", "Atlanta"]
    filtered_restaurant_data = restaurant_data[(restaurant_data["city"] != "Atlanta") | (restaurant_data["province"] == "GA")]
    city_restaurant_data = {city: filtered_restaurant_data[filtered_restaurant_data["city"] == city] for city in cities}
    return city_restaurant_data, cities

# [MAP]
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

# [VIZ2]
def city_dataframe(city_restaurant_data, city_selector):
    st.dataframe(
        data = city_restaurant_data[city_selector],
        height = 600,
        column_config = {
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

# [ST1] need to add ST 2-4
def home_page(city_restaurant_data, cities):
    st.set_page_config(layout="wide")
    st.title("Fast Food Restaurants by City")
    city_selector = st.selectbox("Select a City", cities)
    column1, column2 = st.columns(2)
    with column1:
        st.header = "Interactive Map"
        city_maps(city_restaurant_data, city_selector)
    with column2:
        st.header = "Restaurant Locations"
        city_dataframe(city_restaurant_data, city_selector)

# [VIZ1] and [DA3]
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