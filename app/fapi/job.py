from flask import Blueprint
from test_data import job_data

job_bp = Blueprint("job", __name__, url_prefix="/job")


@job_bp.route('/job_info', methods=["GET"])
def job_info():
    return {"job_info": job_data.job_data}
