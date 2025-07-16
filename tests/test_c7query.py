# test_c7query.py

import json
from c7query import loadConfig, getC7Contacts, getC7Companies, getContactsByCompany, getC7RequirementCandidates
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



def test_getC7RequirementCandidates():

    requirementId = 260
    result = getC7RequirementCandidates(requirementId)
    
    assert result != [], "No candidates returned"


if __name__ == '__main__':
    test_getC7RequirementCandidates()
        
