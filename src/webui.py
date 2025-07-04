import streamlit as st
from classes import Company, Contact
from c7query import getC7Companies, getC7Contacts, getC7Company, getC7Contact

# Helper: fetch and format companies for dropdown
def fetch_companies():
    # Adjust this function if getC7Companies doesn't return a list of dicts
    # Example dummy data, replace with actual function call
    # [{'CompanyId': 1, 'CompanyName': 'Acme Ltd'}, ...]
    result = getC7Companies()  
    
    if result == 200:
        companies = [company_name for eachcompany in Company]
        return companies
        
    return {}

# Helper: fetch and format contacts for dropdown
def fetch_contacts():
    # Adjust this function if getC7Contacts doesn't return a list of dicts
    # [{'ContactId': 1, 'Forenames': 'John', 'Surname': 'Doe'}, ...]
    result = getC7Contacts()
    
    if result == 200:        
        contacts = [{'ContactId': contact.companyid, 'Forenames': contact.surname}
                     for contact in Contact]
        return companies
    
    return {}

st.title("Change Specialists")

companies = fetch_companies()
contacts = fetch_contacts()

company_name = st.selectbox("Select a company", options=list(companies.keys()))
contact_name = st.selectbox("Select a contact", options=list(contacts.keys()))

if company_name:
    company_id = companies[company_name]
    company_info = getC7Company(company_id)
    st.subheader("Company Details")
    st.json(company_info)

if contact_name:
    contact_id = contacts[contact_name]
    contact_info = getC7Contact(contact_id)
    st.subheader("Contact Details")
    st.json(contact_info)
