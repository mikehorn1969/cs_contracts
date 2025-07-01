# c7query.py

import urllib.request, json
import requests
import configparser
#import sys
from classes import Company, Contact

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

        return response.status_code

    except Exception as e:
        print(e)


def getC7Contact(contact_id):

    subscription_key, user_id, api_key = loadConfig()

    try:

        url = f"https://coll7openapi.azure-api.net/api/Contact/Get?UserId={user_id}&ContactId={contact_id}&IncludeArchivedRecords=false"

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
       # companyname, name, address, emailaddress, phone, title
        result = {
            "CompanyName": (response_json.get("CompanyName")),
            "ContactName": (response_json.get("Forenames") or "") + " " + (response_json.get("Surname") or ""),            
            "ContactAddress": (
                (response_json.get("AddressLine1") or "") + " " +
                (response_json.get("AddressLine2") or "") + " " +
                (response_json.get("AddressLine3") or "") + " " +
                (response_json.get("City") or "") + " " +
                (response_json.get("Postcode") or "")
            ).strip(),
            "ContactEmail": response_json.get("EmailAddress") or "",
            "ContactPhone": response_json.get("TelephoneNumber") or "",
            "ContactTitle": response_json.get("Title") or ""
            }

        return response.status_code

    except Exception as e:
        print(e)


def getC7Contacts():
     
    subscription_key, user_id, api_key = loadConfig()

    #try:       
    url = f"https://coll7openapi.azure-api.net/api/Contact/AdvancedSearch"

    hdr ={
    # Request headers
    'Cache-Control': 'no-cache',
    'Ocp-Apim-Subscription-Key': subscription_key,
    }
    body ={
        "userId": user_id,
        "allColumns": False,
        "columns": ["ContactId", "CompanyName", "Forenames", "Surname", "AddressLine1", "AddressLine2", "AddressLine3", 
                    "City", "Postcode", "EmailAddress", "TelephoneNumber", "Title"],
        "includeArchived": False,
        "parameters": [{
            "fieldName": "DateCreated",
            "fieldValue": "1 Jan 2010" 
        }]
    }

    response = requests.post(url, headers=hdr , json=body)

    # Read and decode response
    response_json = response.json()

    # Parse JSON
    # response_json = json.loads(response_body)

    # Extract desired fields
    # companyname, name, address, emailaddress, phone, title
    
    for ContactId, CompanyName, Forenames, Surname, AddressLine1, AddressLine2, Addressline3, City, Postcode, EmailAddress, TelephoneNumber, Title in response_json:

        idx = Contact.counter + 1
        ContactName = f"{Forenames} {Surname}"
        ContactAddress = f"{AddressLine1}, {AddressLine2}, {Addressline3}, {City}, {Postcode}"
            
        new_contact = Contact({CompanyName}, ContactName, ContactAddress, {EmailAddress}, {TelephoneNumber}, {Title})

    # return json.dumps(result)
    return response.status_code

    #except Exception as e:
    #    print(e)


if __name__ == '__main__':
    getC7Contacts()    

    print(f"Contact count: {Contact.counter}")