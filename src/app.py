# app.py

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from c7query import getC7Companies, getContactsByCompany, getC7Contacts
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route('/', methods=["GET", "POST"])
def index():
    
    """ companies = getC7Companies()
    company_names = []
    for company in companies:
        company_names.append(company.get("CompanyName"))

    contact_names = []
    if session.get("selected_company") is None:    
        contacts = getC7Contacts()
    else:
        contacts = getContactsByCompany(session.get("selected_company"))

    for contact in contacts:
        contact_names.append(contact.get("ContactName")) """

    if request.method == "POST":
        selected = request.form.get("company")
        if selected:
            session['selected_company'] = selected
            
        selected = request.form.get("contact")
        if selected:
            session['selected_contact'] = selected
    selected_company = session.get('selected_company')
    selected_contact = session.get('selected_contact')

    return render_template('index.html',items=company_names, selected_item=selected_company, items2=contact_names, selected_item2=selected_contact)

# API endpoint to get all companies (as JSON)
@app.route('/api/companies')
def api_companies():
    companies = getC7Companies()   
    return jsonify(companies)


# API endpoint to get contacts for a company (if you want filtering)
@app.route('/api/contacts')
def api_contacts():
    contacts = getContactsByCompany(session.get('selected_company'))     
    return jsonify(contacts)


if __name__ == '__main__':
    app.run(debug=True)
