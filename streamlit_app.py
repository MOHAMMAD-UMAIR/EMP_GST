import streamlit as st
from pymongo import MongoClient
from data_extraction import *
import pandas as pd
import re


# Assuming you have a MongoDB client connected to your database
#client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_uri = "mongodb+srv://umair:umairmongo@cluster0.pgkqn44.mongodb.net/?retryWrites=true&w=majority"

database_name = "GST_Check"
collection_name = "GST"

client = MongoClient(mongo_uri)
database = client[database_name]
collection_GST = database[collection_name]

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
            #For top 5 results
            #top_5=PAN_results[:5]
            st.table(PAN_results)
            gst_not_in_DB=[]
            for top in PAN_results:
                record_exist = search_record_exist(top["gstin"],collection_GST)
                if record_exist:
                    print("GST number is in DB")
                    
                else:
                    print("GST is not in DB")
                    gst_not_in_DB.append(top["gstin"])
                    
                    
            for gst in gst_not_in_DB:
                status=get_status(gst,PAN_results )
                if status == 'Active' :
                    jamku_extract(gst,collection_GST)
                    print(f"{gst} added in the DB")
            #if st.button("Get Filing details of each GST"):
            for top in PAN_results:
                st.subheader(f"Filing Details for {top['gstin']}")
                if top["sts"] == "Active" :
                    print("Generating table")
                    # Fetch documents where GSTIN is "1234"
                    query = {"gstin": top["gstin"]}
                    result = collection_GST.find(query)

                    # Print or process the fetched documents
                    returns=[]
                    for document in result:
                        returns=document["returns"]
                        
                        
                    # Create a dictionary to store records based on rtntype
                    rtntype_data = {}
                    for record in returns:
                        rtntype = record['rtntype']
                        if rtntype not in rtntype_data:
                            rtntype_data[rtntype] = []
                        
                        # Remove the 'rtntype' key and add the 'check' field
                        record.pop('rtntype', None)
                        # dof_day = int(record['dof'].split('/')[0])
                        # record['check'] = 'Delayed' if dof_day > 15 else 'On time'

                        rtntype_data[rtntype].append(record)
                
                    # Display the records in a Streamlit table
                    for rtntype, records in rtntype_data.items():
                        st.write(f" Filing Details: {rtntype}")
                        df = pd.DataFrame(records)
                        selected_columns = df[['fy', 'taxp','dof','check']]  # List of column names
                        selected_columns.columns = ['Financial Year', 'Tax Period','Date of Filing', 'Check']
                        print(selected_columns)
                        st.table(selected_columns)
                        
                else:
                    st.warning("The GST is not active")        
                            
        else:
            st.warning("No matching records found.")
    else:
        st.warning("Please enter both first and last names to search.")            
        
        