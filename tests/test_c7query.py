# test_sandpit.py

import json
from c7query import loadConfig, getC7Company, getC7Contact, getC7Contacts
from classes import Company, Contact

def test_loadConfig():
    
    result = loadConfig() 

    assert(isinstance(result,tuple)), "loadConfig result should be tuple"

def test_getC7Company():
    
    company_data = getC7Company("5076") # test with CS company number

    company = json.loads(company_data)

    # Print each key-value pair
    print("Output of getCompany():")
    for key, value in company.items():
        print(f"{key}: {value}")

    # Optional: assertion for testing purposes
    assert isinstance(company, dict), "Result should be a dictionary"
    assert "ClientName" in company_data, "Expected key 'ClientName' not found" 
    assert "Jurisdiction" in company_data, "Expected key 'Jurisdiction' not found" 
    assert "ClientCompanyNo" in company_data, "Expected key 'ClientCompanyNo' not found" 
    assert "ClientAddress" in company_data, "Expected key 'ClientAddress' not found" 



def test_getC7Contact():
    
    contact_data = getC7Contact("5306") # test with CS company number

    contact = json.loads(contact_data)

    # Print each key-value pair
    print("Output of getC7Contact():")
    for key, value in contact.items():
        print(f"{key}: {value}")

    assert isinstance(contact, dict), "Result should be a dictionary"

    assert "ContactName" in contact_data, "Expected key 'ContactName' not found" 
    assert "ContactEmail" in contact_data, "Expected key 'ContactEmail' not found"
    assert "ContactPhone" in contact_data, "Expected key 'ContactPhone' not found"
    assert "ContactAddress" in contact_data, "Expected key 'ContactAddress' not found"
    assert "ContactTitle"  in contact_data, "Expected key 'ContactTitle' not found"


def test_getC7Contacts():

    result = getC7Contacts()

    print(f"Contact count: {Contact.counter}")
    print(f"Result: {result}")
    
    assert result == 200, "Failed to load contacts"


if __name__ == '__main__':
    test_getC7Contacts()