import streamlit as st
from .langchain_helper import generate_resturant_name_n_items

st.title("Resturant Name Generator")

country = st.sidebar.selectbox("Pick a Country name for Resturant Name", ("India", "Saudi Arabia", "Mexico", "America", "Bangladesh", "Pakistan", "Afganistan"))

if country:
    response = generate_resturant_name_n_items(country)\
    
    st.header(response['resturant_name'].strip())
    
    st.write("**Menu Items**")
    menu_items = response['items'].split(",").strip()

    for item in menu_items:
        st.write("-", item)