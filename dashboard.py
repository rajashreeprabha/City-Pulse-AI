import streamlit as st
import sqlite3
from backend.area_predict import predict_area

st.title("CityPulse AI – Tamil Nadu Risk Dashboard")

# Connect DB
conn = sqlite3.connect("backend/database.db")
cursor = conn.cursor()

# STEP 3.1: Get all districts of Tamil Nadu
cursor.execute("""
SELECT DISTINCT district FROM city_data_v2
WHERE state = 'Tamil Nadu'
""")

districts = [row[0] for row in cursor.fetchall()]

# If no data yet
if len(districts) == 0:
    st.warning("No reports received from Tamil Nadu yet")
else:
    districts = [
    "Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore",
    "Dharmapuri", "Dindigul", "Erode", "Kallakurichi", "Kanchipuram",
    "Kanniyakumari", "Karur", "Krishnagiri", "Madurai", "Mayiladuthurai",
    "Nagapattinam", "Namakkal", "Nilgiris", "Perambalur", "Pudukkottai",
    "Ramanathapuram", "Ranipet", "Salem", "Sivaganga", "Tenkasi",
    "Thanjavur", "Theni", "Thoothukudi", "Tiruchirappalli", "Tirunelveli",
    "Tirupathur", "Tiruppur", "Tiruvallur", "Tiruvannamalai",
    "Tiruvarur", "Vellore", "Viluppuram", "Virudhunagar"
]

selected_district = st.selectbox("Select District", districts)


if st.button("Check Risk"):
        result = predict_area(selected_district)
        st.subheader(f"{selected_district} Risk Status: {result}")
