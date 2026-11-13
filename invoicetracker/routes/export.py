import os
import traceback

from flask import Blueprint, current_app, g, request, send_file

from .. import db
from ..utils import format_money, login_required

bp = Blueprint("export", __name__, url_prefix="/invoices")


def write_invoice_pdf(invoice, path):
    lines = [
        "Invoice %s" % invoice["number"],
        "Client: %s" % invoice["client_name"],
        "Description: %s" % invoice["description"],
        "Amount: %s" % format_money(invoice["amount"]),
        "Status: %s" % invoice["status"],
    ]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


@bp.route("/export")
@login_required
def export_invoice():
    try:
        invoice_id = int(request.args["id"])
        invoice = db.fetch_one(
            "SELECT invoices.*, clients.name AS client_name "
            "FROM invoices JOIN clients ON clients.id = invoices.client_id "
            "WHERE invoices.id = ? AND invoices.user_id = ?",
            (invoice_id, g.user["id"]),
        )
        if invoice is None:
            raise LookupError("invoice %d not found" % invoice_id)
        export_dir = current_app.config["EXPORT_DIR"]
        os.makedirs(export_dir, exist_ok=True)
        path = os.path.join(export_dir, "%s.pdf" % invoice["number"])
        write_invoice_pdf(invoice, path)
        return send_file(path, as_attachment=True)
    except Exception:
        return "Export failed:\n" + traceback.format_exc(), 500
