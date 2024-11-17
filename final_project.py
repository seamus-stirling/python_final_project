import pandas as pd
import pydeck
import pydeck as pdk
import streamlit as st
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

def city_maps(city_restaurant_data, cities):
    st.header("Fast Food Restaurants by City")
    city_selector = st.selectbox("Select a City", cities)
    st.write("Current City:", city_selector)

    view_state = pdk.ViewState(
        latitude = city_restaurant_data["Boston"]["latitude"].mean(),
        longitude = city_restaurant_data["Boston"]["longitude"].mean(),
        zoom = 11,
        pitch = 0
    ),
    layers = [
        pdk.Layer(
            "HexagonLayer",
            data = city_restaurant_data[city_selector],
            get_position = "[longitude, latitude]",
            get_color = "[255, 0, 0]",
            get_radius = 100,
            )
    ]
    map = pdk.Deck(
        map_style= None,
        intial_view_state = view_state,
        layers = layers
    )
    st.pydeck_chart(map)


    return

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
    city_maps(city_restaurant_data, cities)
main()