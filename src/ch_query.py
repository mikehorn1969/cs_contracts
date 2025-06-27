import requests
from requests.auth import HTTPBasicAuth
import json
from c7query import loadConfig

def CHQuery(companyNo):
    """Get company info by company number using requests library."""
    subscription_key, user_id, api_key = loadConfig()

    if not api_key:
        raise ValueError("API key not found in config file.")

    url = f"https://api.companieshouse.gov.uk/company/{companyNo}"
    
    auth_str = f"{api_key}:" 
  
    response = requests.get(url, auth = (f"{auth_str}",''))

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

