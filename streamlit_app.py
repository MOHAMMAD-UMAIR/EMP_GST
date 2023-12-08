import streamlit as st
from pymongo import MongoClient
from data_extraction import *

import re

# MongoDB connection details
# mongo_uri = "mongodb+srv://umair:umairmongo@cluster0.pgkqn44.mongodb.net/?retryWrites=true&w=majority"
# database_name = "PEP"
# collection_name = "rajya_sabha"


st.title("GST Explorer")

# Get user input for first and last name
PAN_input = st.text_input("Enter PAN", "")

if st.button("Search"):
    if PAN_input :
        st.write(f"Searching for GSTs with PAN: {PAN_input}")
        
        PAN_results = process_master_india(PAN_input)
        
        if PAN_results:
            st.write(f"Total number of registered GSTs: {len(PAN_results)}")
            st.table(PAN_results)
            
        else:
            st.warning("No matching records found.")
    else:
        st.warning("Please enter both first and last names to search.")            
        
        