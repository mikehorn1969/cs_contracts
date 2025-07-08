# app.py

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from c7query import getC7Companies, getC7Contacts, getC7Company, getC7Contact

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected = request.form.get("company")
        if selected:
            session['selected_company'] = selected
            return redirect(url_for("index"))
    selected_item = session.get('selected_item')

    return render_template('index.html',items=items, selected_item=selected_item)

# API endpoint to get all companies (as JSON)
@app.route('/api/companies')
def api_companies():
    companies = getC7Companies()   
    return jsonify(companies)

# API endpoint to get contacts for a company (if you want filtering)
@app.route('/api/contacts')
def api_contacts():
    contacts = getC7Contacts()     
    return jsonify(contacts)

# API endpoint to get a single company by id
@app.route('/api/company/<company_id>')
def api_company(company_id):
    company = getC7Company(company_id)
    return jsonify(company)

# API endpoint to get a single contact by id
@app.route('/api/contact/<contact_id>')
def api_contact(contact_id):
    contact = getC7Contact(contact_id)
    return jsonify(contact)

if __name__ == '__main__':
    app.run(debug=True)
