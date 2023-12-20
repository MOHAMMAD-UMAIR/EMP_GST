import streamlit as st
from pymongo import MongoClient
from data_extraction import *
import pandas as pd
#import re
import io

output = io.BytesIO()

# Use the BytesIO object as the filehandle.
writer = pd.ExcelWriter(output, engine='xlsxwriter')
# Create a bold format
bold_format = writer.book.add_format({'bold': True})

#Mongo DB cridentials
mongo_uri = "mongodb+srv://umair:umairmongo@cluster0.pgkqn44.mongodb.net/?retryWrites=true&w=majority"
database_name = "GST_Check"
collection_name = "GST"

#Establishing mongo connection
client = MongoClient(mongo_uri)
database = client[database_name]
collection_GST = database[collection_name]


#Website title
st.title("GST Explorer")

# Get user input for first and last name
PAN_input = st.text_input("Enter PAN", "")

if st.button("Search"):
    if PAN_input :
        st.write(f"Searching for GSTs with PAN: {PAN_input}")
        
        PAN_results = razor_pay(PAN_input)
        
        if PAN_results:
            print(PAN_input)
            f_name=str(PAN_input)+".xlsx"
            print(f_name)
            r=2
            #writer.write(str(PAN_input), startrow=r )
            st.write(f"Total number of registered GSTs: {len(PAN_results)}")
            #For top 5 results
            #top_5=PAN_results[:5]
            
            
            #converting the json response to data frae for making csv file
            pan_to_gst_df = pd.DataFrame(PAN_results)
            #print(pan_to_gst_df)

            
            # Changing the column names for CSV file
            pan_to_gst_df.columns=["GST", 'Status', "State"]
            #Writing the Data frame of search results in the excel sheet
            pan_to_gst_df.to_excel(writer,sheet_name='Sheet1', startrow=r, index=False )
            
            r=r+len(pan_to_gst_df)+1 #updating the row column pointer based on the results length
            
            #defining worksheet for text entry in excel file
            worksheet = writer.sheets['Sheet1']
            # Create a bold format

            worksheet.write(0, 0, "Search results based on PAN: "+ str(PAN_input))
            
            # Displaying results data frame on front end
            st.table(pan_to_gst_df)
            
            gst_not_in_DB=[]
            for top in PAN_results:
                record_exist = search_record_exist(top["gstin"],collection_GST)
                if record_exist:
                    print("GST number is in DB")
                    
                else:
                    print("GST is not in DB")
                    gst_not_in_DB.append(top["gstin"])
                    
                    
            for gst in gst_not_in_DB:
                
                status=get_status(gst,PAN_results)
                
                if status == 'Active' :
                    jamku_extract(gst,collection_GST)
                    print(f"{gst} added in the DB")
            #if st.button("Get Filing details of each GST"):
            for top in PAN_results:
                st.subheader(f"Filing Details for {top['gstin']}")
                r=r+1
                worksheet.write(r, 0, "Filing details of GST: "+ str(top['gstin']))
                r=r+2
                if top["auth_status"] == "Active" :
                    print("Generating table")
                    # Fetch documents where GSTIN is "1234"
                    query = {"gstin": top["gstin"]}
                    result = collection_GST.find(query)

                    # Print or process the fetched documents
                    returns=[]
                    for document in result:
                        returns=document["returns"]
                        name=document["lgnm"]
                        address=document["adr"]
                        reg_date=document["rgdt"]
                        nba=document["nba"]
                        hsn=document["hsn"]
                    
                    worksheet.write(r, 0, "Business name: ")
                    worksheet.write(r, 1, str(name))
                    r=r+1
                    worksheet.write(r, 0, "Business address: ")
                    worksheet.write(r, 1, str(address))
                    r=r+1
                    worksheet.write(r, 0, "Registration Date: ")
                    worksheet.write(r, 1, str(reg_date))
                    r=r+1
                    worksheet.write(r, 0, "NBA: ")
                    worksheet.write(r, 1, str(nba))
                    r=r+1
                    
                    worksheet.write(r, 0, "HSN: ")
                    worksheet.write(r, 1, str(hsn))
                    r=r+1
                    
                       
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
                        
                        
                        #Adding the columns to the excel sheet
                        r=r+1
                        worksheet.write(r, 0, "Table: "+ str(rtntype))
                        worksheet.write(r, 1,str(rtntype), bold_format )
                        r=r+1
                        selected_columns.to_excel(writer,sheet_name='Sheet1', startrow=r, index=False )
                        r=r+len(selected_columns)+1
                        
                        st.table(selected_columns)
                        
                else:
                    st.warning("The GST is not active")
                    worksheet.write(r, 0, "The GST is not active", bold_format)
                    r=r+2
           
            writer.close()
            xlsx_data2 = output.getvalue()
            print("printing the file name again")
            print(f_name)          
            st.download_button(
                label="Download Excel workbook",
                data=xlsx_data2,
                file_name=f_name,
                mime="application/vnd.ms-excel"
            )                        
        else:
            st.warning("No matching records found.")
    else:
        st.warning("Please enter both first and last names to search.")            
        
        