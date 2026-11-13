from functools import wraps

from flask import g, redirect, session, url_for

from . import db


def sanitize_text(value):
    """Escape a string so it can be placed safely inside HTML."""
    if value is None:
        return ""
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


def format_money(amount):
    return "${:,.2f}".format(amount)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user_id = session.get("user_id")
        if user_id is None:
            return redirect(url_for("auth.login"))
        g.user = db.fetch_one("SELECT id, username FROM users WHERE id = ?", (user_id,))
        if g.user is None:
            session.clear()
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped
