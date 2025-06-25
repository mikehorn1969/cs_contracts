import requests
from requests.auth import HTTPBasicAuth
import base64
import json
from sandpit import loadConfig

def CHQuery(companyNo):
    """Get company info by company number using requests library."""
    subscription_key, user_id, api_key = loadConfig()

    if not api_key:
        raise ValueError("API key not found in config file.")

    # url = f"https://api.company-information.service.gov.uk/company/{companyNo}"
    url = f"https://api.companieshouse.gov.uk/company/{companyNo}"
    
    auth_str = f"{api_key}:" 
    b64_auth_str = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")+':'

    print(f"DBG: request: {url}")

    response = requests.get(url, auth = (f"{auth_str}",''))

    print(f"DBG: response: {response}")

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

