from script1 import get_company

def test_get_company_valid_id():
    result = get_company(1)
    assert result["name"] == "Acme Corp"

def test_get_company_invalid_id():
    result = get_company(999)
    assert "error" in result
