import sqlite3

from flask import current_app


def connect():
    conn = sqlite3.connect(current_app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def fetch_one(sql, params=()):
    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchone()
    finally:
        conn.close()


def fetch_all(sql, params=()):
    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()
    finally:
        conn.close()


def execute(sql, params=()):
    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def find_invoices(where_clause):
    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT invoices.id, invoices.number, invoices.description, invoices.amount, "
            "invoices.status, clients.name AS client_name "
            "FROM invoices JOIN clients ON clients.id = invoices.client_id " + where_clause
        )
        return cursor.fetchall()
    finally:
        conn.close()
