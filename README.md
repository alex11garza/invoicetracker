# InvoiceTracker

A small Flask app for freelancers to keep track of clients and invoices.

## Features

- Log in and see your own invoices
- Search invoices by client, number or description
- Create invoices and update their status (draft, sent, paid, overdue)
- Export an invoice to a file
- Add clients, with a quick preview card

## Running locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
DEMO_PASSWORD=choose-a-password python seed.py
flask --app invoicetracker run
```

Then open http://127.0.0.1:5000 and log in as `maria` or `james` with the password you chose.

## Project layout

```
seed.py               creates a demo database
invoicetracker/
  __init__.py         application factory and blueprint registration
  auth.py             login and logout
  db.py               SQLite helpers
  filters.py          builds the WHERE clause for invoice search
  utils.py            HTML escaping, money formatting, login_required
  schema.sql          database schema
  routes/
    invoices.py       list, view, create and update invoices
    search.py         invoice search
    export.py         invoice export
    clients.py        client list, creation and preview
  templates/          Jinja templates
  static/             stylesheet
```
