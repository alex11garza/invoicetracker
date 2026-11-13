from flask import Blueprint, g, render_template, request

from .. import db
from ..filters import build_filter
from ..utils import format_money, login_required

bp = Blueprint("search", __name__, url_prefix="/invoices")


@bp.route("/search")
@login_required
def search_invoices():
    search = request.args.get("search", "")
    where_clause = build_filter(g.user["id"], search=search)
    invoices = db.find_invoices(where_clause)
    return render_template(
        "invoices.html",
        invoices=invoices,
        search=search,
        format_money=format_money,
    )
