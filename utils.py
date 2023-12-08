import pandas
import json
import requests

def process_jamku(GST):
    # Example JSON data (dictionary)
    
    #is it the right way to do it ?
    json_data = jamku_extract(GST).text


    # Convert JSON string to a Python dictionary
    json_obj = json.loads(json_data)

    # Extract only the "records" data
    records_data = json_obj["data"]

    # Specify the file path
    file_path = str(GST)+".json"

    # Save the "records" data to a new JSON file
    with open(file_path, 'w') as json_file:
        # Use indent for pretty formatting (optional)
        json.dump(records_data, json_file, indent=2)

    print(f"Records data has been saved to {file_path}")
    
    
    
    
    
def jamku_extract(GST):
    url = "https://gst-return-status.p.rapidapi.com/free/gstin/"+str(GST)

    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": "3069be76abmshb67b831fd540c33p19492cjsnb4ebce237db5",
        "X-RapidAPI-Host": "gst-return-status.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    print(f"Connection established with Jamku API for GST: {GST} ")
    
    return response



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
    file_path = str(PAN)+"_to_GST.json"

    # Save the "records" data to a new JSON file
    with open(file_path, 'w') as json_file:
        # Use indent for pretty formatting (optional)
        json.dump(records_data_filtered, json_file, indent=2)

    print(f"Records data has been saved to {file_path}")
    
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