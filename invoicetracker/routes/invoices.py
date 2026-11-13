from flask import Blueprint, abort, g, redirect, render_template, request, url_for

from .. import db
from ..utils import format_money, login_required

bp = Blueprint("invoices", __name__, url_prefix="/invoices")


@bp.route("/")
@login_required
def list_invoices():
    invoices = db.fetch_all(
        "SELECT invoices.id, invoices.number, invoices.description, invoices.amount, "
        "invoices.status, clients.name AS client_name "
        "FROM invoices JOIN clients ON clients.id = invoices.client_id "
        "WHERE invoices.user_id = ? ORDER BY invoices.id DESC",
        (g.user["id"],),
    )
    return render_template("invoices.html", invoices=invoices, format_money=format_money)


@bp.route("/<int:invoice_id>")
@login_required
def view_invoice(invoice_id):
    invoice = db.fetch_one(
        "SELECT invoices.*, clients.name AS client_name, clients.email AS client_email "
        "FROM invoices JOIN clients ON clients.id = invoices.client_id "
        "WHERE invoices.id = ?",
        (invoice_id,),
    )
    if invoice is None:
        abort(404)
    return render_template("invoice.html", invoice=invoice, format_money=format_money)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new_invoice():
    clients = db.fetch_all(
        "SELECT id, name FROM clients WHERE user_id = ? ORDER BY name", (g.user["id"],)
    )
    if request.method == "POST":
        client_id = request.form.get("client_id", type=int)
        owned = db.fetch_one(
            "SELECT id FROM clients WHERE id = ? AND user_id = ?", (client_id, g.user["id"])
        )
        if owned is None:
            abort(400)
        count = db.fetch_one(
            "SELECT COUNT(*) AS n FROM invoices WHERE user_id = ?", (g.user["id"],)
        )["n"]
        invoice_id = db.execute(
            "INSERT INTO invoices (user_id, client_id, number, description, amount, status) "
            "VALUES (?, ?, ?, ?, ?, 'draft')",
            (
                g.user["id"],
                client_id,
                "INV-%04d" % (count + 1),
                request.form.get("description", ""),
                request.form.get("amount", 0, type=float),
            ),
        )
        return redirect(url_for("invoices.view_invoice", invoice_id=invoice_id))
    return render_template("new_invoice.html", clients=clients)


@bp.route("/<int:invoice_id>/status", methods=["POST"])
@login_required
def update_status(invoice_id):
    status = request.form.get("status")
    if status not in {"draft", "sent", "paid", "overdue"}:
        abort(400)
    db.execute(
        "UPDATE invoices SET status = ? WHERE id = ? AND user_id = ?",
        (status, invoice_id, g.user["id"]),
    )
    return redirect(url_for("invoices.view_invoice", invoice_id=invoice_id))
