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

# [PY3], [DA1], [DA9] Takes the raw data that I downloaded and reorganized and puts it into a dataframe only using the important info columns
def read_data(csv_file):
    try:
        restaurant_data = pd.read_csv(csv_file, usecols=[1,2,3,4,5,6,7,8,9])
        restaurant_data["Full Address"] = restaurant_data.apply(lambda row: f"{row['address']}, {row['city']}, {row['province']}", axis=1)
        return restaurant_data
    except Exception as e:
        st.error("Error: The file is either empty, unreadable, or missing a column")


# [PY2], [PY4], [PY5], and [DA5] Using the restaurant data and my city list I read all of the data for the corresponding city into a dictionary
def city_splitter(restaurant_data):
    cities = ["Boston", "New York", "Los Angeles", "Philadelphia", "Atlanta", "Houston", "Seattle"]
    filtered_restaurant_data = restaurant_data[(restaurant_data["city"] != "Atlanta") | (restaurant_data["province"] == "GA")]
    city_restaurant_data = {city: filtered_restaurant_data[filtered_restaurant_data["city"] == city] for city in cities}
    return city_restaurant_data, cities


# [DA2] and [DA7]
def most_locations(restaurant_data):
    locations = restaurant_data.groupby("name").size().sort_values(ascending=False)
    top_5 = locations.head(5).index.tolist()
    top_5_data = restaurant_data[restaurant_data["name"].isin(top_5)]
    return top_5_data

def top_5_map(top_5_data):
    selection = st.multiselect("Restaurants", ["McDonald's", "Burger King", "Arby's", "Taco Bell", "Subway"], default= ["McDonald's", "Burger King", "Arby's", "Taco Bell", "Subway"])
    filtered_top_5_data = top_5_data[top_5_data["name"].isin(selection)]
    logo_sources = {
        "McDonald's": "https://github.com/seamus-stirling/python_final_project/blob/64c94145e164fc0a53b8dbe4cd053892faa4e128/mcd_logo.png",
        "Burger King": "bk_logo.png",
        "Arby's": "arby_logo.png",
        "Taco Bell": "tbell_logo.png",
        "Subway": "subway_logo.png"
    }

    filtered_top_5_data["icon_data"] = filtered_top_5_data["name"].map(logo_sources)

    view_state = pdk.ViewState(
        latitude=float(top_5_data["latitude"].mean()),
        longitude=float(top_5_data["longitude"].mean()),
        zoom=4,
        pitch=0
    )
    icon_data = {
        "url": "https://i.postimg.cc/HsjRhqrj/Mcdonalds-Logo.png",
        "width": 128,
        "height": 128,
        "anchorY": 128
    }
    layer_1 = pdk.Layer(
                "ScatterplotLayer",
                data= filtered_top_5_data,
                get_color="[255, 0, 0]",
                get_radius=150,
                get_position=["longitude", "latitude"],
                pickable=True
            )
    layer_2 = pdk.Layer(
                "IconLayer",
                data= filtered_top_5_data,
                get_icon= icon_data,
                get_position=["longitude", "latitude"],
                get_size = 15,
                pickable=True
            )
    tool_tip = {"html": "{name} <br> {Full Address}",
                "style": {
                    "backgroundColor": "steelblue",
                    "color": "white",
                    "fontSize": "12px"
                    }
                }
    map = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=view_state,
        layers= [layer_2],
        tooltip=tool_tip
    )
    st.subheader("The 5 Restaurants with the Most Locations")
    st.pydeck_chart(map, height=600)
    st.dataframe(filtered_top_5_data)


# [MAP] and [ST3] This function displays a map based on the chosen city
def city_maps(city_restaurant_data, city_selector):
    st.write("Current City:", city_selector)
    selected_city = city_selector
    view_state = pdk.ViewState(
        latitude = float(city_restaurant_data[selected_city]["latitude"].mean()),
        longitude = float(city_restaurant_data[selected_city]["longitude"].mean()),
        zoom = 12,
        pitch = 0
    )
    layer = [
        pdk.Layer(
            "ScatterplotLayer",
            data = city_restaurant_data[selected_city],
            get_position = ["longitude", "latitude"],
            get_color = "[255, 0, 0]",
            get_radius = 150,
            pickable = True
            )
    ]
    tool_tip = {"html": "{name} <br> {Full Address}",
                "style": {
                    "backgroundColor": "steelblue",
                    "color": "white",
                    "fontSize": "12px"
                    }
                }
    map = pdk.Deck(
        map_style ="mapbox://styles/mapbox/light-v9",
        initial_view_state = view_state,
        layers = layer,
        tooltip = tool_tip
    )
    st.pydeck_chart(map, height=600)



# This function shows all the fast food restaurants nationwide
def popularity_map(restaurant_data):
    view_state = pdk.ViewState(
        latitude=float(restaurant_data["latitude"].mean()),
        longitude=float(restaurant_data["longitude"].mean()),
        zoom=2,
        pitch=0
    )
    layer = [
        pdk.Layer(
            "ScatterplotLayer",
            data= restaurant_data,
            get_position=["longitude", "latitude"],
            get_color="[255, 0, 0]",
            get_radius=250,
            pickable=True
        )
    ]
    tool_tip = {"html": "{name} <br> {Full Address}",
                "style": {
                    "backgroundColor": "steelblue",
                    "color": "white",
                    "fontSize": "12px"
                    }
                }
    map = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=view_state,
        layers=layer,
        tooltip=tool_tip
    )
    st.header("All Fast Food Locations")
    st.pydeck_chart(map, height=600)


# [VIZ2] and [ST2] This function sets the parameters for the city dataframe and provides a button to download the info as a csv
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
            "country": "Country",
            "postalCode": "Zip Code",
            "latitude":"Latitude",
            "longitude": "Longitude"
        }
    )
    st.download_button(
        label="Download this data as a CSV",
        data= city_restaurant_data[city_selector].to_csv(index=False),
        file_name=city_selector + "_Fast_Food_Restaurants.csv",
        mime="text/csv"
    )

def location_bar_chart(restaurant_data):
    states = restaurant_data["province"].unique()
    selected_states = st.selectbox("State Selection", states)
    filtered_data = restaurant_data[restaurant_data["province"] == selected_states]
    location_counts = filtered_data.groupby("name")["name"].count().reset_index(name="Location Count")
    location_counts = location_counts.sort_values(by="Location Count", ascending= False)
    st.bar_chart(
        data=location_counts,
        x = "name",
        y = "Location Count"
    )


# [ST1] need to add ST 2-4
def home_page(city_restaurant_data, cities, restaurant_data):
    st.set_page_config(page_title="Fast Food Restaurants by City" , layout="wide")
    tab1, tab2, tab3 = st.tabs(["All Fast Food Locations", "View and Download Specific City Data", "Most Popular Fast Food Restaurants"])
    st.logo = (
        "https://i.postimg.cc/HsjRhqrj/Mcdonalds-Logo.png"
    )
    with tab1:
        popularity_map(restaurant_data)
    with tab2:
        st.header("View and Download Specific City Data")
        city_selector = st.selectbox("Select a City", cities)
        column1, column2 = st.columns(2)
        with column1:
            st.subheader("Interactive Map")
            city_maps(city_restaurant_data, city_selector)
        with column2:
            st.subheader("Restaurant Locations")
            city_dataframe(city_restaurant_data, city_selector)
    with tab3:
        st.header("Most Popular Fast Food Chains and Their Locations")
        top_5_map(most_locations(restaurant_data))
        location_bar_chart(restaurant_data)


def main():
    csv_file = "fast_food_usa.csv"
    restaurant_data = read_data(csv_file)
    city_restaurant_data, cities = city_splitter(restaurant_data)
    home_page(city_restaurant_data, cities, restaurant_data)


main()
