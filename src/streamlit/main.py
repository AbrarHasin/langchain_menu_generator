import streamlit as st
import sys
from pathlib import Path

# Add the current directory to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent))

from langchain_helper import generate_resturant_name_n_items

st.title("Resturant Name Generator")

country = st.sidebar.selectbox("Pick a Country name for Resturant Name", ("India", "Saudi Arabia", "Mexico", "America", "Bangladesh", "Pakistan", "Afganistan"))

if country:
    response = generate_resturant_name_n_items(country)\
    
    st.header(response['resturant_name'].strip())
    
    st.write("**Menu Items**")
    menu_items = response['menu_items'].strip().split(",")

    for item in menu_items:
        st.write("-", item)