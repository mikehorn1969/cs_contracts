# test_c7query.py

import json
from c7query import loadConfig, getC7Contacts, getC7Companies, getContactsByCompany
from classes import Config, Company, Contact

def test_loadConfig():
    
    result = loadConfig() 

    assert(result == "Config Loaded"), "loadConfig failed"


def test_getC7Contacts():

    result = getC7Contacts()

    print(f"Contact count: {Contact.counter}")
    print(f"Result: {result}")
    
    assert result == 200, "Failed to load contacts"


def test_getC7Companies():

    result = getC7Companies()

    print(f"Company count: {Company.counter}")
    

    #assert result == 200, "Failed to load contacts"


def test_getContactsByCompany():

    company_name = "Bellrock Property and Facilities Management"
    result = getContactsByCompany(Company)



if __name__ == '__main__':
    test_getC7Companies()
        