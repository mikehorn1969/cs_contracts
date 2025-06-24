# test_sandpit.py

import json
import src
from sandpit import loadConfig, getCompany

def test_loadConfig():
    
    result = loadConfig() 

    assert(isinstance(result,tuple)), "loadConfig result should be tuple"

def test_getCompany():
    
    company_data = getCompany("5076") # test with CS company number

    company = json.loads(company_data)

    # Print each key-value pair
    print("Output of getCompany():")
    for key, value in company.items():
        print(f"{key}: {value}")

    # Optional: assertion for testing purposes
    assert isinstance(company, dict), "Result should be a dictionary"
    assert "CompanyName" in company_data, "Expected key 'CompanyName' not found" 


"""
ClientName

ClientCompanyNo
ClientAddress
"""