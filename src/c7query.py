# c7query.py - Colleague 7 API queries

import json
import requests
import configparser
from classes import Company, Contact
import re

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

        response = requests.get(url, headers=hdr)

        # Parse JSON
        response_json = response.json()
        
        # Extract desired fields
        # companyname, address
        RawAddress = (response_json.get("AddressLine1") or "") + ", " + (response_json.get("AddressLine2") or "") + ", " + (response_json.get("AddressLine3") or "") + ", " + (response_json.get("City") or "") + ", " + (response_json.get("Postcode") or "")
        CompanyAddress = re.sub(r',+', ',', RawAddress)    # strip extra commas where an address field was empty

        result = {
            "CompanyName": response_json.get("CompanyName"),
            "CompanyAddress": CompanyAddress
        }

        return result

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

        response = requests.get(url, headers=hdr)

        # Parse JSON
        response_json = response.json()

        # Extract desired fields
        # companyname, name, address, emailaddress, phone, title

        ContactName = (response_json.get("forenames") or "") + " " + (response_json.get("surname") or "")
        RawAddress = (response_json.get("AddressLine1") or "") + ", " + (response_json.get("AddressLine2") or "") + ", " + (response_json.get("AddressLine3") or "") + ", " + (response_json.get("City") or "") + ", " + (response_json.get("Postcode") or "")
        ContactAddress = re.sub(r',+', ',', RawAddress)    # strip extra commas where an address field was empty

        result = {
            "CompanyName": (response_json.get("CompanyName")),
            "ContactName": ContactName,
            "ContactAddress": ContactAddress,
            "ContactEmail": response_json.get("EmailAddress") or "",
            "ContactPhone": response_json.get("TelephoneNumber") or "",
            "ContactTitle": response_json.get("Title") or ""
            }

        return result

    except Exception as e:
        print(e)


def getC7Contacts():
     
    subscription_key, user_id, api_key = loadConfig()

    try:       
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

        # Extract desired fields
        # companyname, name, address, emailaddress, phone, title    
        contacts = []
        for ContactId, CompanyName, Forenames, Surname, AddressLine1, AddressLine2, Addressline3, City, Postcode, EmailAddress, TelephoneNumber, Title in response_json:

            ContactName = f"{Forenames} {Surname}"
            RawAddress = f"{AddressLine1}, {AddressLine2}, {Addressline3}, {City}, {Postcode}"
            ContactAddress = re.sub(r',+', ',', RawAddress)    # strip extra commas where an address field was empty
            new_contact = Contact({CompanyName}, ContactName, ContactAddress, {EmailAddress}, {TelephoneNumber}, {Title})

            contacts.append({
                "ContactId": ContactId,
                "CompanyName": CompanyName,
                "ContactName": ContactName,
                "ContactAddress": ContactAddress,
                "ContactEmail": EmailAddress,
                "ContactPhone": TelephoneNumber,
                "ContactTitle": Title
            })

        return contacts

    except Exception as e:
        return e
    
def getC7Companies():
    
    subscription_key, user_id, api_key = loadConfig()

    try:       
        url = f"https://coll7openapi.azure-api.net/api/Company/AdvancedSearch"

        hdr ={
        # Request headers
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': subscription_key,
        }
        body ={
            "userId": user_id,
            "allColumns": False,
            "columns": ["CompanyId", "CompanyName", "AddressLine1", "AddressLine2", "AddressLine3", 
                        "City", "Postcode", "telephoneNumber", "companyEmail", "registrationNumber"],
            "includeArchived": False,
            "parameters": [{
                "fieldName": "DateCreated",
                "fieldValue": "1 Jan 2010" 
            }]
        }

        response = requests.post(url, headers=hdr , json=body)

        # Read and decode response
        response_json = response.json()

        # Extract desired fields
        # companyname, name, address, emailaddress, phone, title    
        companies = []
        for CompanyId, CompanyName, AddressLine1, AddressLine2, Addressline3, City, Postcode, companyEmail, TelephoneNumber, registrationNumber in response_json:

            RawAddress = f"{AddressLine1}, {AddressLine2}, {Addressline3}, {City}, {Postcode}"
            CompanyAddress = re.sub(r',+', ',', RawAddress)    # strip extra commas where an address field was empty
                
            # create a new Company instance
            new_contact = Company({CompanyName}, CompanyAddress, {companyEmail}, {TelephoneNumber}, {registrationNumber})

            companies.append({
                "CompanyId": CompanyId,
                "CompanyName": CompanyName,
                "CompanyAddress": CompanyAddress,
                "CompanyEmail": companyEmail,
                "CompanyPhone": TelephoneNumber,
                "CompanyNumber": registrationNumber
            })

        return companies

    except Exception as e:
        return e


if __name__ == '__main__':
    getC7Companies()    
