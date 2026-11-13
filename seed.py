"""Create a local database with demo users, clients and invoices."""

import os
import sqlite3
import sys

from werkzeug.security import generate_password_hash

HERE = os.path.dirname(os.path.abspath(__file__))
PACKAGE_DIR = os.path.join(HERE, "invoicetracker")
DB_PATH = os.environ.get("INVOICETRACKER_DB", os.path.join(PACKAGE_DIR, "invoicetracker.db"))

DEMO_USERS = {
    "maria": [
        ("Brightside Bakery", "orders@brightside.example", [
            ("Website redesign, phase 1", 1800.00, "paid"),
            ("Online ordering integration", 950.00, "sent"),
        ]),
        ("Lakeview Dental", "office@lakeview.example", [
            ("Appointment booking widget", 600.00, "overdue"),
        ]),
    ],
    "james": [
        ("Northwind Logistics", "it@northwind.example", [
            ("Shipment tracking dashboard", 4200.00, "sent"),
            ("API maintenance (October)", 750.00, "draft"),
        ]),
    ],
}


def main():
    password = os.environ.get("DEMO_PASSWORD")
    if not password:
        sys.exit("Set DEMO_PASSWORD to the password the demo accounts should use.")

    conn = sqlite3.connect(DB_PATH)
    with open(os.path.join(PACKAGE_DIR, "schema.sql"), encoding="utf-8") as fh:
        conn.executescript(fh.read())

    for username, clients in DEMO_USERS.items():
        user_id = conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        ).lastrowid
        count = 0
        for name, email, invoices in clients:
            client_id = conn.execute(
                "INSERT INTO clients (user_id, name, email) VALUES (?, ?, ?)",
                (user_id, name, email),
            ).lastrowid
            for description, amount, status in invoices:
                count += 1
                conn.execute(
                    "INSERT INTO invoices (user_id, client_id, number, description, amount, status) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (user_id, client_id, "INV-%04d" % count, description, amount, status),
                )

    conn.commit()
    conn.close()
    print("Created %s" % DB_PATH)


if __name__ == "__main__":
    main()
