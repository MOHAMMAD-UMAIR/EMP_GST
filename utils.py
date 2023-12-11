import pandas as pd
import json
import requests
from datetime import datetime


# the filling dates of all the GST forms

filing_records = {
    "GSTR3B": {'July': '20/8/2023',
               'June': '20/7/2023',
               'May': '20/06/2023',
               'April': '24/05/2023',
               'March': '20/04/2023',
               'February': '20/03/2023',
               'January': '20/02/2023',
               'December': '20/01/2024',
               'November': '20/12/2023',
               'October': '20/11/2023',
               'September': '21/10/2023',
               'August': '20/9/2023'},
    
    "GSTR1IFF": {'July': '11/8/2023',
                 'June': '11/7/2023',
                 'May': '11/06/2023',
                 'April': '11/05/2023',
                 'March': '11/04/2023',
                 'February': '11/03/2023',
                 'January': '11/02/2023',
                 'December': '11/01/2024',
                 'November': '11/12/2023',
                 'October': '11/11/2023',
                 'September': '11/10/2023',
                 'August': '11/9/2023'},
    
    "GSTR9": {'2021-2022': '31/12/2022',
              '2020-2021': '28/02/2022',
              '2019-2020': '31/03/2021',
              '2018-2019': '31/12/2020',
              '2017-2018': '12/02/2020'},
    
    "GSTR9C": {'2021-2022': '31/12/2022',
               '2020-2021': '28/02/2022',
               '2019-2020': '31/03/2021',
               '2018-2019': '31/12/2020',
               '2017-2018': '12/02/2020'},  #17/01/2020
            
    
    "GSTR1": {'July': '11/8/2023',
              'June': '11/7/2023',
              'May': '11/06/2023',
              'April': '11/05/2023',
              'March': '11/04/2023',
              'February': '11/03/2023',
              'January': '11/02/2023',
              'December': '11/01/2024',
              'November': '11/12/2023',
              'October': '11/11/2023',
              'September': '11/10/2023',
              'August': '11/9/2023'},
    
    "GSTR6": {'July': '13/8/2023',
              'June': '13/7/2023',
              'May': '13/06/2023',
              'April': '13/05/2023',
              'March': '13/04/2023',
              'February': '13/03/2023',
              'January': '13/02/2023',
              'December': '13/01/2024',
              'November': '13/12/2023',
              'October': '13/11/2023',
              'September': '13/10/2023',
              'August': '13/9/2023'},
    
    "GSTR10": {'2021-2022': '23/04/2023',
               '2020-2021': '28/02/2022',
               '2019-2020': '31/03/2021',
               '2018-2019': '31/12/2020',
               '2017-2018': '12/02/2021'},
    
    "GSTR7": {'July': '10/8/2023',
              'June': '10/7/2023',
              'May': '10/06/2023',
              'April': '10/05/2023',
              'March': '10/04/2023',
              'February': '10/03/2023',
              'January': '10/02/2023',
              'December': '10/01/2024',
              'November': '10/12/2023',
              'October': '10/11/2023',
              'September': '10/10/2023',
              'August': '10/9/2023'},
    
    "GSTR8": {'July': '10/8/2023',
        'June': '10/7/2023',
        'May': '10/06/2023',
        'April': '10/05/2023',
        'March': '10/04/2023', 
        'February': '10/03/2023',
        'January': '10/02/2023', 
        'December': '10/01/2024',
        'November': '10/12/2023',
        'October': '10/11/2023',
        'September': '10/10/2023',
        'August': '10/9/2023'}
    }





''' This function checks weather a gst record is already there in the DB
'''
def search_record_exist(GST, collection_GST):
    
    existing_record = collection_GST.find_one({"gstin": GST})
    
    return existing_record
    



# def process_jamku(GST,collection_GST,client):
#     # Example JSON data (dictionary)
    
#     #is it the right way to do it ?
#     json_data = jamku_extract(GST)

    
#     # Convert JSON string to a Python dictionary
#     json_obj = json.loads(json_data)

#     # Extract only the "records" data
#     records_data = json_obj["data"]
    
    
    
    

#     # # Specify the file path
#     # file_path = str(GST)+".json"

    # # Save the "records" data to a new JSON file
    # with open(file_path, 'w') as json_file:
    #     # Use indent for pretty formatting (optional)
    #     json.dump(records_data, json_file, indent=2)

    # print(f"Records data has been saved to {file_path}")
    
    
    
    
    
def jamku_extract(GST, collection_GST):
    print(str(GST))
    url = "https://gst-return-status.p.rapidapi.com/free/gstin/"+str(GST)

    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": "3069be76abmshb67b831fd540c33p19492cjsnb4ebce237db5",
        "X-RapidAPI-Host": "gst-return-status.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    json_data=response.text
    print(f"Connection established with Jamku API for GST: {GST} ")
    
    # Convert JSON string to a Python dictionary
    json_obj = json.loads(json_data)

    # Extract only the "records" data
    records_data = json_obj["data"]
    
    updated_at_timestamp = datetime.utcnow().isoformat()

    records_data["updated_at"]=updated_at_timestamp
    
    
    #code for calculating the delay check
    
    # Key-Value Dictionary

    # Update the 'check' key and value in the JSON data
    returns_data = records_data.get("returns", [])
    for return_obj in returns_data:
        return_name=return_obj.get("rtntype", "")
        
        fy = return_obj.get("fy", "")
        dof = return_obj.get("dof", "")
        filing_table=filing_records.get(return_name,"")
        #filing_date = pd.to_datetime(filing_table.get(fy, ""), format='%dd/%mm/%YYYY')
        #return_obj["check"] = 'Delayed' if pd.to_datetime(dof, format='%dd/%mm/%YYYY') > filing_date else 'On time'
        
        if fy and dof:  # Check if fy and dof are not empty
            period=return_obj.get("taxp", "")
            if period == 'Annual':
                filing_date = pd.to_datetime(filing_table.get(fy, ""), format='%d/%m/%Y')
                print(f'the filing date is :{filing_date}')
                filed_date=pd.to_datetime(dof, format='%d/%m/%Y')
                if filed_date > filing_date:
                    return_obj["check"] = 'Delayed'
                    print("greater tahn loop ran")
                else:
                    return_obj["check"] = 'On Time'
                    print('smaller than loop ran')
                date=pd.to_datetime(dof, format='%d/%m/%Y')
                print(f'the submitted date is : {date}')
            else:
                filing_date = pd.to_datetime(filing_table.get(period, ""), format='%d/%m/%Y')
                return_obj["check"] = 'Delayed' if pd.to_datetime(dof, format='%d/%m/%Y') > filing_date else 'On time'
                
        else:
            return_obj["check"] = 'Invalid'

    # Create DataFrame
    df = pd.DataFrame(returns_data)

    # Display the DataFrame
    #print(df)

    # Update original JSON data with new fields from DataFrame
    records_data["returns"] = df.to_dict(orient='records')

    # Display the updated JSON data
    print(records_data)
    
    
    # Insert records into the MongoDB collection
    collection_GST.insert_one(records_data)

    print(f"Records have been inserted into the GST collection for {GST} ")
    
    



def process_master_india(PAN):
    # Example JSON data (dictionary)
    json_data = master_india_extract(PAN)

    # Convert JSON string to a Python dictionary
    json_obj = json.loads(json_data)["data"]

    # Extract only the "data" data
    #records_data = json_obj["data"]
    # Keep only "stjCd" and "lgnm" keys
    keys_to_keep = ["gstin","sts"]
    
    records_data_filtered = [{key: element.get(key) for key in keys_to_keep} for element in json_obj]

    #print(records_data_filtered)

    # Specify the file path
    #file_path = str(PAN)+"_to_GST.json"

    # Save the "records" data to a new JSON file
    # with open(file_path, 'w') as json_file:
    #     # Use indent for pretty formatting (optional)
    #     json.dump(records_data_filtered, json_file, indent=2)

    #print(f"Records data has been saved to {file_path}")
    
    return records_data_filtered
    
    


def master_india_extract(PAN):
    url = "https://blog-backend.mastersindia.co/api/v1/custom/search/name_and_pan/?keyword="+str(PAN)

    headers = {
    'authority': 'blog-backend.mastersindia.co',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en;q=0.9,ur-IN;q=0.8,ur;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'origin': 'https://www.mastersindia.co',
    'pragma': 'no-cache',
    'referer': 'https://www.mastersindia.co/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    response_master_india = requests.request("GET", url, headers=headers)
    master_data = response_master_india.text

    print(f"Established connection  to the master india website for the PAN:{PAN}")
    
    return master_data


# getting gst status

def get_status(gst_value, gst_data):
    for record in gst_data:
        if record['gstin'] == gst_value:
            return record['sts']
    return 'GST not found'



