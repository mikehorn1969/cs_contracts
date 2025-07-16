# app.py

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from c7query import getC7Companies, getContactsByCompany, getC7Requirements, getC7RequirementCandidates
from classes import Company, Contact, Requirement
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route('/', methods=["GET", "POST"])
def index():
    
    companies = getC7Companies()
    company_names = [company["CompanyName"] for company in companies]

    contact_names = [] 
    req_names = []
    candidate_names = []

    selected_company = session.get('selected_company', '')
    selected_contact = session.get('selected_contact', '')
    selected_requirement = session.get('selected_requirement')
    selected_candidate = session.get('selected_candidate')

    if request.method == "POST":
        if 'btCompany' in request.form:
            selected_company = request.form.get("company")
            session['selected_company'] = selected_company
            session['selected_contact'] = ''
            return redirect(url_for('index'))

        if 'btContact' in request.form:
            selected_contact = request.form.get('contact')
            session['selected_contact'] = selected_contact
            session['selected_requirement'] = ''
            return redirect(url_for('index'))
        
        if 'btRequirement' in request.form:
            selected_requirement = request.form.get('requirement')
            session['selected_requirement'] = selected_requirement
            session['selected_candidate'] = ''
            return redirect(url_for('index'))
        
        if 'btCandidate' in request.form:
            selected_candidate = request.form.get('candidate')
            session['selected_candidate'] = selected_candidate
            return redirect(url_for('index'))

    # Only show contacts if a company is selected
    if selected_company:
        contacts = getContactsByCompany(selected_company)
        contact_names = [contact.get("ContactName") for contact in contacts]

    # Only show requirements once a contact has been selected
    if selected_contact:
        requirements = getC7Requirements(selected_company, selected_contact)
        req_names = [requirement.get("Description") for requirement in requirements]

    # Only show candidates once a requirement has been selected
    if selected_requirement:
        id_part, name_part = selected_requirement.split(" - ",1)
        candidates = getC7RequirementCandidates(id_part)
        candidate_names = [candidate.get("Name") for candidate in candidates]

    return render_template(
        'index.html',
        company_names=company_names,
        selected_company=selected_company,
        contact_names=contact_names,
        selected_contact=selected_contact,
        requirements=req_names,
        selected_requirement=selected_requirement,
        candidate_names=candidate_names,
        selected_candidate=selected_candidate
    )


# API endpoint to get all companies (as JSON)
@app.route('/api/companies')
def api_companies():
    companies = getC7Companies()   
    return jsonify(companies)


# API endpoint to get contacts for a company
@app.route('/api/contacts')
def api_contacts():
    contacts = getContactsByCompany(session.get('selected_company'))     
    return jsonify(contacts)


# API endpoint to get requirements for a company/contact
@app.route('/api/requirements')
def api_requirements():
    requirements = getC7Requirements(session.get('selected_company'),session.get('selected_contact'))     
    return jsonify(requirements)


# API endpoint to get requirements for a company/contact
@app.route('/api/candidates')
def api_candidates():

    reqname = f"{session.get('selected_requirement')}"
    requestId = reqname.split(" - ",1)

    candidates = getC7RequirementCandidates(requestId)     
    return jsonify(candidates)


if __name__ == '__main__':
    app.run(debug=True)
