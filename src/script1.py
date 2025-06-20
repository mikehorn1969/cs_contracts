def get_company(company_id):
    """Simulates retrieving company information."""
    dummy_data = {
        1: {"name": "Acme Corp", "location": "London"},
        2: {"name": "Globex Ltd", "location": "Manchester"},
        3: {"name": "Initech", "location": "Birmingham"}
    }

    return dummy_data.get(company_id, {"error": "Company not found"})
