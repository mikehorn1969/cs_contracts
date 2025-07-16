# test_c7query.py

import json
from c7query import loadConfig, getC7Contacts, getC7Companies, getContactsByCompany, getC7Requirements
from classes import Company

def test_loadConfig():
    
    result = loadConfig() 

    assert(result == "Config Loaded"), "loadConfig failed"


def test_getC7Contacts():

    result = getC7Contacts()
    
    assert result != [], "No contacts returned"



def test_getC7Companies():

    result = getC7Companies()
  
    assert result != [], "No companies returned"



def test_getContactsByCompany():

    company_name = "Bellrock Property and Facilities Management"
    result = getContactsByCompany(company_name)

    assert result != [], "No contacts returned"



def test_getC7Requirements():

    company_name = "Bellrock Property and Facilities Management"
    contact_name = "Matt Langelier"
    result = getC7Requirements(company_name,contact_name)
    
    for req in result:
        print(f"{req.get('RequirementId')} {req.get('Description')}")

    #assert result != [], "No requirements returned"


if __name__ == '__main__':
    test_getC7Requirements()
        
