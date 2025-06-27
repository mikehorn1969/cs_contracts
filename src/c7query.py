# sandpit.py

import urllib.request, json
import configparser
import sys

def loadConfig():

    # Read config
        config = configparser.ConfigParser()
        files_read = config.read("colleague7.cfg")
        
        # Get subscription key from config
        subscription_key = config.get('APIKEYS', 'SUBSCRIPTION_KEY1')    
        user_id = config.get('APIKEYS', 'C7_USERID')
        ch_key = config.get('APIKEYS', 'CH_KEY')

        return(subscription_key, user_id, ch_key)

def getC7Company(company_id):

    subscription_key, user_id, api_key = loadConfig()

    try:

        url = f"https://coll7openapi.azure-api.net/api/Company/Get?UserId={user_id}&CompanyId={company_id}&IncludeArchivedRecords=false"

        hdr ={
        # Request headers
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': subscription_key,
        }

        req = urllib.request.Request(url, headers=hdr)

        req.get_method = lambda: 'GET'
        response = urllib.request.urlopen(req)

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


def getC7Contact(contact_id):

    subscription_key, user_id, api_key = loadConfig()

    try:

        url = f"https://coll7openapi.azure-api.net/api/Contact/Get?UserId={user_id}&CompanyId={contact_id}&IncludeArchivedRecords=false"

        hdr ={
        # Request headers
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': subscription_key,
        }

        req = urllib.request.Request(url, headers=hdr)

        req.get_method = lambda: 'GET'
        response = urllib.request.urlopen(req)

        # Read and decode response
        response_body = response.read().decode('utf-8')

        # Parse JSON
        response_json = json.loads(response_body)

       # Extract desired fields
        result = {
            "ContactName": response_json.get("Forenames") + " " + response_json.get("Surname"),
            "ContactEmail": response_json.get("EmailAddress"),
            "ContactPhone": response.json.get("TelephoneNumber"),           
            "ContactAddress": response_json.get("AddressLine1") + " " + response_json.get("AddressLine2") + " " + response_json.get("AddressLine3") + " " +response_json.get("City") + " " + response_json.get("Postcode"),
            "ContactTitle": response_json.get("Title")
        }

        return json.dumps(result)

    except Exception as e:
        print(e)
