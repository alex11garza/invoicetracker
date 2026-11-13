import os
import secrets

from flask import Flask, redirect, url_for

from .auth import bp as auth_bp
from .routes.clients import bp as clients_bp
from .routes.export import bp as export_bp
from .routes.invoices import bp as invoices_bp
from .routes.search import bp as search_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    app.config["DATABASE"] = os.environ.get(
        "INVOICETRACKER_DB", os.path.join(app.root_path, "invoicetracker.db")
    )
    app.config["EXPORT_DIR"] = os.environ.get(
        "INVOICETRACKER_EXPORTS", os.path.join(app.root_path, "exports")
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(clients_bp)

    @app.route("/")
    def index():
        return redirect(url_for("invoices.list_invoices"))

    return app
