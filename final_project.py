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
        "McDonald's": "https://i.postimg.cc/HsjRhqrj/Mcdonalds-Logo.png",
        "Burger King": "https://i.postimg.cc/02Sz3Cb1/bk-logo.png",
        "Arby's": "https://i.postimg.cc/wxZt0rxk/arby-logo.png",
        "Taco Bell": "https://i.postimg.cc/MpbvZK7s/tbell-logo.png",
        "Subway": "https://i.postimg.cc/qvdNdC3h/subway-logo.png"
    }
    filtered_top_5_data["icon_data"] = filtered_top_5_data["name"].map(
        lambda name: {
            "url": logo_sources.get(name, ""),
            "width": 128,
            "height": 128,
            "anchorY": 128
        }
    )
    view_state = pdk.ViewState(
        latitude=float(top_5_data["latitude"].mean()),
        longitude=float(top_5_data["longitude"].mean()),
        zoom=4,
        pitch=0
    )
    layer = pdk.Layer(
        "IconLayer",
        data= filtered_top_5_data,
        get_icon= "icon_data",
        get_size= 4,
        size_scale = 15,
        get_position=["longitude", "latitude"],
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
        layers= layer,
        tooltip=tool_tip
    )
    st.subheader("The 5 Restaurants with the Most Locations")
    st.pydeck_chart(map, height=600)


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
        zoom=3,
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
    states = sorted(restaurant_data["province"].unique())
    selected_states = st.selectbox("State Selection", states)
    filtered_data = restaurant_data[restaurant_data["province"] == selected_states]
    location_counts = filtered_data.groupby("name")["name"].count().reset_index(name="Location Count").sort_values(by="Location Count", ascending=False).set_index("name")
    column3, column4 = st.columns([1, 4])
    with column3:
        st.subheader("Chart Data")
        st.dataframe(
            location_counts,
            use_container_width=True
        )
    with column4:
        st.bar_chart(
            data= location_counts,
            use_container_width=True,
            x_label="Fast Food Chains",
            y_label="Number of Locations",
            height=600
        )


# [ST1] need to add ST 2-4
def home_page(city_restaurant_data, cities, restaurant_data):
    st.set_page_config(page_title="Fast Food Restaurants by City" , layout="wide")
    tab0, tab1, tab2, tab3, tab4 = st.tabs(["Welcome Page", "All Fast Food Locations", "View and Download Specific City Data", "The 5 Most Popular Fast Food Chains","Fast Food Restaurants by State"])
    with tab0:
        st.header("Welcome to my final program for CS230!")
        st.subheader("Description:")
        st.write("This web app explores a data file containing 10,000 fast food restaurants nation. You can navigate through the app by using the tabs at the top of the page. Each different tab showcases the data in a different way so feel free to explore! If you would like to download the data that I used for this project please click the button below to download the CSV file.")
        st.download_button(
            label="Download this data as a CSV",
            data="fast_food_usa.csv",
            file_name="fast_food_usa.csv",
            mime="text/csv"
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
        st.header("The 5 Most Popular Fast Food Chains")
        top_5_map(most_locations(restaurant_data))
    with tab4:
        st.header("Fast Food Restaurants by State")
        location_bar_chart(restaurant_data)


def main():
    csv_file = "fast_food_usa.csv"
    restaurant_data = read_data(csv_file)
    city_restaurant_data, cities = city_splitter(restaurant_data)
    home_page(city_restaurant_data, cities, restaurant_data)


main()
