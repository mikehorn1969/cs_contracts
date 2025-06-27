# Initialise_MergeData.py
'''
script to initialise data connections for 
  Colleague 7 API
  Companies House API
'''

import configparser
import sys
import requests
import json

# Read config
config = configparser.ConfigParser()
files_read = config.read("colleague7.cfg")

# Get subscription key from config
subscription_key = config.get('APIKEYS', 'SUBSCRIPTION_KEY1')    
user_id = config.get('APIKEYS', 'C7_USERID')
ch_key = config.get('APIKEYS', 'CH_KEY')

def CHQuery(companyNo):
    """Get company info by company number using requests library."""

    url = f"https://api.companieshouse.gov.uk/company/{companyNo}"
    
    auth_str = f"{ch_key}:" 
  
    response = requests.get(url, auth = (f"{auth_str}",''))

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def getC7Company(company_id):

    try:

        url = f"https://coll7openapi.azure-api.net/api/Company/Get?UserId={user_id}&CompanyId={company_id}&IncludeArchivedRecords=false"
        hdr ={
        # Request headers
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': subscription_key,
        }

        response = requests.get(url, headers=hdr)

        # Read and decode response
        response_body = response.read().decode('utf-8')

        # Parse JSON
        response_json = json.loads(response_body)

       # Extract desired fields
        result = {
            "CompanyName": response_json.get("CompanyName"),
            "AddressId": response_json.get("AddressId"),
            "AddressLine1": response_json.get("AddressLine1"),
            "AddressLine2": response_json.get("AddressLine2"),
            "AddressLine3": response_json.get("AddressLine3"),
            "City": response_json.get("City"),
            "County": response_json.get("County"),
            "Country": response_json.get("Country"),
            "Postcode": response_json.get("Postcode"),
        }

        return json.dumps(result)

    except Exception as e:
        print(e)

