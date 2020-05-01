from flask import Blueprint
from test_data import resume_data

resume_bp = Blueprint("resume", __name__, url_prefix="/resume")


@resume_bp.route('/resume_info', methods=["GET"])
def resume_info():
    res = {"resume_info": resume_data.resume_data}
    return res
