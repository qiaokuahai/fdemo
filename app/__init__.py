from flask import Flask
from app import fapi


def create_app():
    app = Flask(__name__)
    curr_bps = fapi.get_curr_bps()
    for _, bp in curr_bps.items():
        app.register_blueprint(bp)
    return app


