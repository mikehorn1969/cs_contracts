# c7query.py - Colleague 7 API queries

import json
import requests
from classes import Company, Contact, Config, Requirement, Candidate
from helper import loadConfig
import re



def getC7Company(company_id):
    
    if Config.find_by_name("C7 Key") is None:
        loadConfig()

    subscription_key = Config.find_by_name("C7 Key")
    user_id = Config.find_by_name("C7 Userid")

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

    if Config.find_by_name("C7 Key") is None:
        loadConfig()

    subscription_key = Config.find_by_name("C7 Key")
    user_id = Config.find_by_name("C7 Userid")

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
     
    if Config.find_by_name("C7 Key") is None:
        loadConfig()

    subscription_key = Config.find_by_name("C7 Key")
    user_id = Config.find_by_name("C7 Userid")

    try:       
        url = f"https://coll7openapi.azure-api.net/api/Contact/AdvancedSearch"

        # Request headers
        hdr ={
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
        response_json = response.json()

        contacts = []
        for item in response_json:
            ContactId = item.get("ContactId", "")
            CompanyName = item.get("CompanyName", "")
            Forenames = item.get("Forenames", "")
            Surname = item.get("Surname", "")
            AddressLine1 = item.get("AddressLine1", "")
            AddressLine2 = item.get("AddressLine2", "")
            Addressline3 = item.get("AddressLine3", "")
            City = item.get("City", "")
            Postcode = item.get("Postcode", "")
            EmailAddress = item.get("EmailAddress", "")
            TelephoneNumber = item.get("TelephoneNumber", "")
            Title = item.get("Title", "")

            ContactName = (Forenames or "") + " " + (Surname  or "")
            RawAddress = (AddressLine1 or "") + ", " + (AddressLine2 or "") + ", " + (Addressline3 or "") + ", " + (City or "") + ", " + (Postcode or "")
            
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
    
    if Config.find_by_name("C7 Key") is None:
        loadConfig()

    subscription_key = Config.find_by_name("C7 Key")
    user_id = Config.find_by_name("C7 Userid")

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
        for item in response_json:
            AddressLine1 = item.get("AddressLine1", "")
            AddressLine2 = item.get("AddressLine2", "")
            AddressLine3 = item.get("AddressLine3", "")
            City = item.get("City", "")
            CompanyEmail = item.get("CompanyEmail", "")
            CompanyId = item.get("CompanyId", "")
            CompanyName = item.get("CompanyName", "")
            Postcode = item.get("Postcode", "")
            RegistrationNumber = item.get("RegistrationNumber", "")
            TelephoneNumber = item.get("TelephoneNumber", "")
        
            RawAddress = (AddressLine1 or "") + ", " + (AddressLine2 or "") + ", " + (AddressLine3 or "") + ", " + (City or "") + ", " + (Postcode or "")
            CompanyAddress = re.sub(r',+', ',', RawAddress)    # strip extra commas where an address field was empty
                
            # create a new Company instance
            new_contact = Company({CompanyName}, CompanyAddress, {CompanyEmail}, {TelephoneNumber}, {RegistrationNumber})

            companies.append({
                "CompanyId": CompanyId,
                "CompanyName": CompanyName,
                "CompanyAddress": CompanyAddress,
                "CompanyEmail": CompanyEmail,
                "CompanyEmail": CompanyEmail,
                "CompanyPhone": TelephoneNumber,
                "CompanyNumber": RegistrationNumber
            })

        return companies

    except Exception as e:
        return e
    

def getContactsByCompany(CompanyName):

    if Config.find_by_name("C7 Key") is None:
        loadConfig()

    subscription_key = Config.find_by_name("C7 Key")
    user_id = Config.find_by_name("C7 Userid")

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
                "fieldName": "CompanyName",
                "fieldValue": CompanyName 
            }]
        }

        response = requests.post(url, headers=hdr , json=body)
        response_json = response.json()

        contacts = []
        for item in response_json:
            ContactId = item.get("ContactId", "")
            CompanyName = item.get("CompanyName", "")
            Forenames = item.get("Forenames", "")
            Surname = item.get("Surname", "")
            AddressLine1 = item.get("AddressLine1", "")
            AddressLine2 = item.get("AddressLine2", "")
            Addressline3 = item.get("AddressLine3", "")
            City = item.get("City", "")
            Postcode = item.get("Postcode", "")
            EmailAddress = item.get("EmailAddress", "")
            TelephoneNumber = item.get("TelephoneNumber", "")
            Title = item.get("Title", "")

            ContactName = (Forenames or "") + " " + (Surname  or "")
            RawAddress = (AddressLine1 or "") + ", " + (AddressLine2 or "") + ", " + (Addressline3 or "") + ", " + (City or "") + ", " + (Postcode or "")
            
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

def getC7Requirements(company_name,contact_name):

    if Config.find_by_name("C7 Key") is None:
        loadConfig()

    subscription_key = Config.find_by_name("C7 Key")
    user_id = Config.find_by_name("C7 Userid")
    notStatus = "Dead"

    try:               
        url = f"https://coll7openapi.azure-api.net/api/Requirement/Search?UserId={user_id}&CompanyName={company_name}&ContactName={contact_name}"

        hdr ={
        # Request headers
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': subscription_key,
        }
        
        response = requests.get(url, headers=hdr)
        response_json = response.json()

        requirements = []
        for item in response_json:

            # ignore dead requirements
            if item.get("statusCode") in notStatus:
                continue

            RequirementId = item.get("requirementId", "")
            CompanyName = item.get("companyName", "")
            ContactName = item.get("contactName", "")
            Description = item.get("entityDescription", "")
            JobTitle = item.get("jobTitle", "")

            new_requirement = Requirement(RequirementId, CompanyName, ContactName, Description, JobTitle)

            displayDesc = f"{RequirementId} - {Description}"

            requirements.append({
                "RequirementId": RequirementId,
                "CompanyName": CompanyName,
                "ContactName": ContactName,
                "Description": displayDesc,
                "JobTitle": JobTitle
            })

        return requirements

    except Exception as e:
        return e


def getC7RequirementCandidates(requirementId):
    
    if Config.find_by_name("C7 Key") is None:
        loadConfig()
        
    subscription_key = Config.find_by_name("C7 Key")
    user_id = Config.find_by_name("C7 Userid")

    try:       
        url = f"https://coll7openapi.azure-api.net/api/Requirement/GetRequirementCandidates?UserId={user_id}&RequirementId={requirementId}"

        hdr ={
        # Request headers
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': subscription_key,
        }
 
        response = requests.get(url, headers=hdr)

        # Read and decode response
        response_json = response.json()

        # Extract desired fields
        # companyname, name, address, emailaddress, phone, title    
        candidates = []
        for item in response_json:
            CandidateId = item.get("CandidateId", "")
            Name = item.get("Name", "")
                
            # create a new Company instance
            new_candidate = Candidate({CandidateId}, {Name} )

            candidates.append({
                "CandidateId": CandidateId,
                "Name": Name
            })

        return candidates

    except Exception as e:
        return e


if __name__ == '__main__':
    
    requirement_id = 260

    result = getC7RequirementCandidates(requirement_id)
    
    for reqfile in result:
        print(f"{reqfile.get('Name')} {reqfile.get('CandidateId')}")
