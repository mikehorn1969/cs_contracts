# test_c7query.py

import json
from c7query import loadConfig, getC7Company, getC7Contact, getC7Contacts, getC7Companies
from classes import Company, Contact

def test_loadConfig():
    
    result = loadConfig() 

    assert(isinstance(result,tuple)), "loadConfig result should be tuple"


def test_getC7Company():
    
    company_id = 915

    company_data = getC7Company(company_id) # test with CS company number

    # Optional: assertion for testing purposes
    assert isinstance(company_data, dict), "Result should be a dictionary"
    assert "CompanyName" in company_data, "Expected key 'CompanyNamentName' not found" 
    assert "CompanyAddress" in company_data, "Expected key 'CompanyAddress' not found" 


def test_getC7Contact():
    
    contact_id = 5306

    contact_data = getC7Contact(contact_id) # test with CS company number

    # Print each key-value pair
    print("Output of getC7Contact():")
    for key, value in contact_data.items():
        print(f"{key}: {value}")

    assert isinstance(contact_data, dict), "Result should be a dictionary"

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


def test_getC7Companies():

    result = getC7Companies()

    print(f"Company count: {Company.counter}")
    print(f"Result: {result}")
    
    assert result == 200, "Failed to load contacts"


if __name__ == '__main__':
    test_getC7Companies()
        