import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_option_menu import option_menu
from streamlit_folium import st_folium  # ✅ Updated import
from datetime import datetime, date
import pandas as pd
import os
import re, base64
from PIL import Image

# Sidebar navigation 🚕
with st.sidebar:
    selected = option_menu(
        menu_title='Anaman Concierge Services',
        options=['Home', 'View Locations', 'Contact Us'],
        menu_icon='cast',
        default_index=0,
        orientation='vertical'
    )

def sanitize_name(name):
    return re.sub(r'[^A-Za-z0-9_]', '_', name)

# Separate list of Iowa City hotels close to Main UI Healthcare with $7.5 base charge
close_to_uihc_hotels = [
    "Courtyard Iowa City University Heights",
    "Heartland Inn",
    "Element Iowa City",
    "Graduate by Hilton Iowa City",
    "Hilton Garden Inn Iowa City Downtown University",
    "hotelVetro Iowa City, Tapestry Collection by Hilton",
    "Hyatt Place Iowa City Downtown"
]

# Data for hotels and hospitals
locations = {
    "Iowa City": {
        "hotels": [
            {"name": "Courtyard Iowa City University Heights", "lat": 41.65635, "lon": -91.55153},
            {"name": "Element Iowa City", "lat": 41.65767, "lon": -91.53296},
            {"name": "Graduate by Hilton Iowa City", "lat": 41.65866, "lon": -91.53273},
            {"name": "Hilton Garden Inn Iowa City Downtown University", "lat": 41.65729, "lon": -91.53370},
            {"name": "hotelVetro Iowa City, Tapestry Collection by Hilton", "lat": 41.6600, "lon": -91.5300},
            {"name": "Hyatt Place Iowa City Downtown", "lat": 41.6600, "lon": -91.5300},
            {"name": "Hotel Chauncey Iowa City, Tapestry Collection by Hilton", "lat": 41.600, "lon": -91.52901}, 
            {"name": "Hampton Inn Iowa City/University Area", "lat": 41.6600, "lon": -91.5300},
            {"name": "Iowa House Hotel CLOSED", "lat": 41.6600, "lon": -91.5300},    
            {"name": "Drury Inn & Suites Iowa City Coralville", "lat": 41.6600, "lon": -91.5300},   
            {"name": "Super 8 by Wyndham Iowa City/Coralville", "lat": 41.6600, "lon": -91.5300},
            {"name": "The Brown Street Inn", "lat": 41.6600, "lon": -91.5300},
            {"name": "Historic Phillips House", "lat": 41.6600, "lon": -91.5300},
            {"name": "Alexis Park Inn", "lat": 41.6600, "lon": -91.5300},   
            {"name": "Travelodge by Wyndham Iowa City", "lat": 41.6600, "lon": -91.5300},
            {"name": "The Highlander Hotel", "lat": 41.6600, "lon": -91.5300}     
        ],
        "hospitals": [
            {"name": "Main UI Healthcare - UI Health Care Medical Center", "lat": 41.65941, "lon": -91.54793},
            {"name": "University of Iowa Health Care Iowa City - First Avenue", "lat": 41.66508, "lon": -91.50192},
            {"name": "UI Health Care, Iowa City, Jefferson Street, Heart Care", "lat": 41.66327, "lon": -91.52708},
            {"name": "UI Health Care–North Dodge", "lat": 41.67818, "lon": -91.51521},
            {"name": "Family Medicine, Iowa City, First Avenue", "lat": 41.66508, "lon": -91.50192},
            {"name": "University of Iowa Health Care Iowa City Northgate Drive", "lat": 41.68753, "lon": -91.48920},
            {"name": "University of Iowa Health Care Sports Medicine", "lat": 41.65981, "lon": -91.57772},
            {"name": "UI Health Care - Scott Blvd", "lat": 41.66790, "lon": -91.48123},
            {"name": "University of Iowa Health Care Medical Center Downtown", "lat": 41.66446, "lon": -91.52841},
            {"name": "Quick Care – Mormon Trek", "lat": 41.65206, "lon": -91.57566},
            {"name": "UI QuickCare – Old Capitol Town Center", "lat": 41.65898, "lon": -91.53402}  
        ]
    },
    "Coralville": {
        "hotels": [
            {"name": "Heartland Inn", "lat": 41.66980, "lon": -91.55805},
            {"name": "SureStay Plus by Best Western Coralville Iowa City", "lat": 41.67601, "lon": -91.56701},
            {"name": "Super 7 Motel", "lat": 41.68109, "lon": -91.56672},
            {"name": "Comfort Inn & Suites Coralville - Iowa City near Iowa River Landing", "lat": 41.68151, "lon": -91.56712},
            {"name": "Staybridge Suites Iowa City - Coralville, an IHG Hotel", "lat": 41.68135, "lon": -91.56163},
            {"name": "Quality Inn Coralville - Iowa River Landing", "lat": 41.68216, "lon": -91.56666},
            {"name": "Hyatt Regency Coralville Hotel & Conference Center", "lat": 41.68190, "lon": -91.55845},
            {"name": "Homewood Suites by Hilton Coralville - Iowa River Landing, IA", "lat": 41.68276, "lon": -91.56178},
            {"name": "Holiday Inn Express & Suites Coralville, an IHG Hotel", "lat": 41.68766, "lon": -91.60390},
            {"name": "Residence Inn Coralville", "lat": 41.686890, "lon": -91.60868},
            {"name": "La Quinta Inn & Suites by Wyndham Coralville Iowa City", "lat": 41.68807, "lon": -91.61127},
            {"name": "Hampton Inn Iowa City/Coralville", "lat": 41.68812, "lon": -91.56508},
            {"name": "SpringHill Suites Coralville", "lat": 41.68846, "lon": -91.60228},
            {"name": "Radisson Hotel & Conference Center Coralville - Iowa City", "lat": 41.68829, "lon": -91.56516},
            {"name": "Fairfield Inn & Suites Coralville", "lat": 41.68600, "lon": -91.61131},
            {"name": "AmericInn by Wyndham Coralville", "lat": 41.70113, "lon": -91.60704},
            {"name": "Country Inn & Suites by Radisson, Coralville", "lat": 41.69985, "lon": -91.60904},
            {"name": "MainStay Suites Coralville - Iowa City", "lat": 41.69798, "lon": -91.60358},
            {"name": "Holiday Inn Express", "lat": 41.6850, "lon": -91.6100}
        ],
        "hospitals": [
            {"name": "Pediatric Associates of University of Iowa Stead Family Children’s Hospital", "lat": 41.70071, "lon": -91.60533},
            {"name": "UI Health Care, Urgent Care, Holiday Road", "lat": 41.70051, "lon": -91.60475},
            {"name": "Iowa KidSight", "lat": 41.70659, "lon": -91.60941},
            {"name": "University of Iowa Health Care Coralville - Heartland Drive", "lat": 41.70202, "lon": -91.60983},
            {"name": "University of Iowa Health Care Coralville - Oakdale Road", "lat": 41.70472, "lon": -91.58957},
            {"name": "University of Iowa Health Care - Iowa River Landing", "lat": 41.68216, "lon": -91.56352},
            {"name": "University of Iowa Health Care Iowa River Landing East", "lat": 41.6850, "lon": -91.6100},
            {"name": "Mother's Milk Bank Of Iowa", "lat": 41.67030, "lon": -91.56642},
            {"name": "University of Iowa Health Network Rehabilitation Hospital", "lat": 41.70815, "lon": -91.61041}
        ]
    },
    "North Liberty": {
        "hotels": [
            {"name": "Sleep Inn", "lat": 41.7490, "lon": -91.6080},
            {"name": "Hampton Inn", "lat": 41.7475, "lon": -91.6105}
        ],
        "hospitals": [
            {"name": "MercyCare North Liberty Urgent Care", "lat": 41.75286, "lon": -91.62841},
            {"name": "University of Iowa Stead Family Children's Hospital North Liberty", "lat": 41.75296, "lon": -91.62868},
            {"name": "MercyCare North Liberty - Family Medicine", "lat": 41.75305, "lon": -91.62863}
        ]
    }
}

def is_off_business_hours(trip_datetime):
    hour = trip_datetime.hour
    is_weekend = trip_datetime.weekday() >= 5
    return is_weekend or (hour < 6 or hour >= 22)

def calculate_fare(hotel_suburb, hotel_name, hospital_suburb, hospital_name, num_people, trip_datetime):
    if hotel_suburb != hospital_suburb and ("North Liberty" in [hotel_suburb, hospital_suburb]):
        base_fare = 15.0 if num_people == 1 else num_people * 7.5
    elif hotel_suburb == "North Liberty" and hospital_suburb == "North Liberty":
        base_fare = 10.0 if num_people == 1 else num_people * 7.5
    elif hotel_suburb == hospital_suburb:
        if hotel_suburb == "Iowa City":
            if hospital_name == "Main UI Healthcare - UI Health Care Medical Center" and hotel_name in close_to_uihc_hotels:
                base_fare = 7.5 * num_people
            else:
                base_fare = 10.0 if num_people == 1 else num_people * 7.5
        else:
            base_fare = 10.0 if num_people == 1 else num_people * 7.5
    else:
        base_fare = 10.0 if num_people == 1 else num_people * 7.5

    if is_off_business_hours(trip_datetime):
        if num_people == 1:
            base_fare += 5.0
        else:
            base_fare = num_people * 7.5

    return base_fare

# -------------------------------
# HOME TAB
# -------------------------------
if selected == "Home":
    st.title("Hotel-Hospital Transportation Cost Calculator")

    st.header("Select Hotel")
    col1, col2 = st.columns(2)
    with col1:
        hotel_suburb = st.selectbox("Hotel Area", list(locations.keys()), key="hotel_suburb")
    with col2:
        hotel_names = [h["name"] for h in locations[hotel_suburb]["hotels"]]
        selected_hotel = st.selectbox("Hotel", hotel_names, key="hotel")

    st.header("Select Hospital")
    col3, col4 = st.columns(2)
    with col3:
        hospital_suburb = st.selectbox("Hospital Area", list(locations.keys()), key="hospital_suburb")
    with col4:
        hospital_names = [h["name"] for h in locations[hospital_suburb]["hospitals"]]
        selected_hospital = st.selectbox("Hospital", hospital_names, key="hospital")

    num_people = st.number_input("Number of People", min_value=1, value=1, step=1)

    st.header("Select Trip Date and Time")
    col5, col6 = st.columns(2)
    with col5:
        trip_date = st.date_input("Trip Date", value=date.today())
    with col6:
        if "trip_time" not in st.session_state:
            st.session_state.trip_time = datetime.now().time()
        trip_time = st.time_input("Trip Time", key="trip_time")

    trip_datetime = datetime.combine(trip_date, trip_time)
    fare = calculate_fare(hotel_suburb, selected_hotel, hospital_suburb, selected_hospital, num_people, trip_datetime)

    if fare is not None:
        st.markdown(
            f"""
            <div style='padding: 20px; background-color: #e0f2f1; border-radius: 10px; margin: 20px 0;'>
                <span style='font-size: 24px; font-weight: bold; color: #004d40;'>Total Fare:</span>
                <span style='font-size: 28px; font-weight: bold; color: #d32f2f; margin-left: 10px;'>${fare:.2f}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.header("Map of Hotels and Hospitals")
    m = folium.Map(location=[41.6611, -91.5300], zoom_start=12)
    hotel_cluster = MarkerCluster(name="Hotels").add_to(m)
    hospital_cluster = MarkerCluster(name="Hospitals").add_to(m)

    for suburb in locations:
        for hotel in locations[suburb]["hotels"]:
            folium.Marker(
                location=[hotel["lat"], hotel["lon"]],
                popup=hotel["name"],
                icon=folium.Icon(color="blue", icon="hotel", prefix="fa")
            ).add_to(hotel_cluster)
        for hospital in locations[suburb]["hospitals"]:
            folium.Marker(
                location=[hospital["lat"], hospital["lon"]],
                popup=hospital["name"],
                icon=folium.Icon(color="red", icon="hospital", prefix="fa")
            ).add_to(hospital_cluster)

    folium.LayerControl().add_to(m)
    st_folium(m, width=700, height=500)  # ✅ UPDATED CALL

# -------------------------------
# VIEW LOCATIONS TAB
# -------------------------------
if selected == "View Locations":
    with st.container():
        st.title("UI Hospital Locations")
        hospitals = [
            (suburb, hospital)
            for suburb, data in locations.items()
            for hospital in data["hospitals"]
        ]
        col1, col2, col3 = st.columns(3)
        for idx, (suburb, hospital) in enumerate(hospitals):
            col = [col1, col2, col3][idx % 3]
            maps_url = f"https://www.google.com/maps/search/?api=1&query={hospital['lat']},{hospital['lon']}"
            sanitized_name = sanitize_name(hospital['name'])
            image_filename = sanitized_name + ".jpg"
            image_path = f"images/{image_filename}"

            with col:
                if os.path.exists(image_path):
                    image_html = f"<img src='data:image/jpeg;base64,{base64.b64encode(open(image_path, 'rb').read()).decode()}' style='width:100%; height:200px; object-fit:cover; border-radius:10px 10px 0 0;'/>"
                else:
                    image_html = ""

                st.markdown(f"""
                    <div style='width: 100%; max-width: 300px; height: 400px; border: 2px solid #ccc; border-radius: 12px; overflow: hidden; padding: 0; margin-bottom: 20px; background: #fff;'>
                        {image_html}
                        <div style='padding: 15px;'>
                            <h5 style='margin-bottom: 5px;'>{hospital['name']}</h4>
                            <p style='margin: 0;'>📍 Located in {suburb}</p>
                            <p style='margin: 5px 0;'>
                                <a href='{maps_url}' target='_blank' style='color: blue; text-decoration: none;'>
                                    ↗️ Get Directions
                                </a>
                            </p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)


# -------------------------------
# CONTACT US TAB
# -------------------------------
if selected == "Contact Us":
    st.title("Contact Us")
    st.markdown("""
    ## Anaman Concierge Services
    **Phone:** 📞 (123) 456-7890  
    **Email:** 📧 reservations@anamancs.com  
    **Address:** 🏢 123 Main Street, Iowa City, IA  

    ### Connect with Us
    [![Facebook](https://img.icons8.com/ios-filled/24/000000/facebook-new.png)](https://www.facebook.com/anamancs/) 
    [![LinkedIn](https://img.icons8.com/ios-filled/24/000000/linkedin.png)](https://linkedin.com) 
    [![Google Maps](https://img.icons8.com/ios-filled/24/000000/google-maps.png)](https://maps.google.com)
    """)
