import urllib.request, json
import base64
import os
import pytest

from ch_query import CHQuery

def test_CHQuery():

    companyNo = "08320269"
        
    try:
        company_data = CHQuery(companyNo)

        print("here 2")
        print(f"output from getCompany: {company_data}")

        print(json.dumps(company_data, indent=2))
    except Exception as e:
        print(f"Failed to get company info: {e}")


if __name__ == "__main__":
    test_CHQuery()