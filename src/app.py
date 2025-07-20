# app.py

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from c7query import getC7Clients, getContactsByCompany, getC7Requirements, getC7RequirementCandidates
from chquery import getCHRecord
import secrets
from classes import Company, Contact, Requirement, Candidate

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route('/', methods=["GET", "POST"])
def index():
    
    clients = getC7Clients()

    client_names = [client["CompanyName"] for client in clients]
    client_fields = ['companyname', 'address', 'emailaddress', 'phone', 'companyNumber']
    client_record = []


    contact_names = [] 
    contact_fields = ['name', 'title', 'address', 'emailaddress', 'phone']
    contact_record = []

    req_names = []
    req_fields = ['companyname', 'contactname', 'description', 'jobtitle']
    req_record = []

    candidate_names = []
    candidate_fields = ['candidateId', 'candidateName', 'companyNumber']
    candidate_record = []

    ch_record = None
    ch_no = ""
    ch_fields = ['company_number', 'company_name', 'company_status']
    selected_company = session.get('selected_company', '')
    selected_contact = session.get('selected_contact', '')
    selected_requirement = session.get('selected_requirement', '')
    selected_candidate = session.get('selected_candidate', '')

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
        
        if 'btCHLookup' in request.form:            
            ch_no = request.form.get('ch_no', '').strip()
            if ch_no:
                try:
                    result = getCHRecord(ch_no)
                    ch_record = {k: result.get(k,'') for k in ch_fields}
                except Exception as e:
                    error = str(e)
            else:
                error = "Please enter a company number."

    # Only show client details and contacts if a company is selected
    if selected_company:
        contacts = getContactsByCompany(selected_company)
        contact_names = [contact.get("ContactName") for contact in contacts]

        try:
            result = Company.find_by("companyname", selected_company)
            client_record = {k: result.__getattribute__(k) for k in client_fields}
        except Exception as e:
            error = str(e)


    # Only show contact details and requirements once a contact has been selected
    if selected_contact:
        requirements = getC7Requirements(selected_company, selected_contact)
        req_names = [requirement.get("Description") for requirement in requirements]

        try:
            result = Contact.find_by("name", selected_contact)            
            contact_record = {k: result.__getattribute__(k) for k in contact_fields}
        except Exception as e:
            error = str(e)


    # Only show candidates once a requirement has been selected
    if selected_requirement:
        id_part = selected_requirement.split(" - ",1)[0]
        candidates = getC7RequirementCandidates(id_part)
        candidate_names = [candidate.get("Name") for candidate in candidates]

        try:
            req_description = (selected_requirement,"-")[0]
            req_description = req_description.lstrip('0123456789- ')

            result = Requirement.find_by("description", req_description)            
            req_record = {k: result.__getattribute__(k) for k in req_fields}
        except Exception as e:
            error = str(e)


    # Only show candidates once a requirement has been selected
    if selected_candidate:
        candidate_name = selected_candidate

        try:
            result = Candidate.find_by("candidateName", candidate_name)            
            candidate_record = {k: result.__getattribute__(k) for k in candidate_fields}
        except Exception as e:
            error = str(e)


    return render_template(
        'index.html',
        client_names=client_names,
        selected_company=selected_company,
        contact_names=contact_names,
        selected_contact=selected_contact,
        requirements=req_names,
        selected_requirement=selected_requirement,
        candidate_names=candidate_names,
        selected_candidate=selected_candidate,
        ch_record=ch_record,
        ch_no=ch_no,
        ch_fields=ch_fields,
        client_fields=client_fields,
        client_record=client_record,
        contact_record=contact_record,
        contact_fields=contact_fields,
        req_fields=req_fields,
        req_record=req_record,
        candidate_fields=candidate_fields,
        candidate_record=candidate_record
    )


# API endpoint to get all clients (as JSON)
@app.route('/api/clients')
def api_clients():
    clients = getC7Clients()   
    return jsonify(clients)


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
