from flask import Blueprint, g, redirect, render_template, request, url_for

from .. import db
from ..utils import login_required, sanitize_text

bp = Blueprint("clients", __name__, url_prefix="/clients")


@bp.route("/")
@login_required
def list_clients():
    clients = db.fetch_all(
        "SELECT id, name, email FROM clients WHERE user_id = ? ORDER BY name",
        (g.user["id"],),
    )
    return render_template("clients.html", clients=clients)


@bp.route("/new", methods=["POST"])
@login_required
def new_client():
    db.execute(
        "INSERT INTO clients (user_id, name, email) VALUES (?, ?, ?)",
        (g.user["id"], request.form.get("name", ""), request.form.get("email", "")),
    )
    return redirect(url_for("clients.list_clients"))


@bp.route("/preview")
@login_required
def preview_client():
    client_name = request.args.get("client_name", "")
    safe_name = sanitize_text(client_name)
    html = (
        "<div class='client-card'>"
        "<h3>" + safe_name + "</h3>"
        "<p>New client &middot; no invoices yet</p>"
        "</div>"
    )
    return html
