# test_sandpit.py

import json
import src
from sandpit import loadConfig, getCompany

def test_loadConfig():
    
    result = loadConfig() 

    assert(True)

def test_getCompany_output():
    
    result = getCompany("5076") # test with CS company number

    """   # Print each key-value pair
    print("Output of csh():")
    for key, value in result.items():
        print(f"{key}: {value}") """

    # Optional: assertion for testing purposes
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "CompanyName" in result, "Expected key 'CompanyName' not found"

    assert(True)

