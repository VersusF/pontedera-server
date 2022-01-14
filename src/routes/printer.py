import os
import bcrypt
from flask import Blueprint, render_template, request
from services import PrinterService, TokenService
from functools import wraps

printer = Blueprint("printer", __name__, template_folder="../templates")
SERVER_LOCAL_IP = "192.168.178.69"
ALLOWED_EXTENSIONS = {"pdf"}


def check_logged(function):
    """
    Preprocessing of route to check if the request is authenticated
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        token = str(request.headers.get("auth"))
        if TokenService.check_token(token):
            return function(*args, **kwargs)
        else:
            return {"error": "Unauthorized"}, 401
    return wrapper


def allowed_file(filename):
    """
    Check file type
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@printer.route("", methods=["GET"])
def main():
    return render_template("printer.html")


@printer.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    pwd: str = body["password"]
    if not pwd:
        return {"error": "Missing password"}, 401
    pwd_bytes = pwd.encode("utf8")
    pwd_hash = os.getenv("PRINTER_PWD").encode("utf8")
    if bcrypt.checkpw(pwd_bytes, pwd_hash):
        token = TokenService.generate_token()
        return {
            "token": token
        }, 201
    else:
        return {"error": "Wrong password"}, 401


@printer.route("/check-token", methods=["GET"])
@check_logged
def check_token():
    return "", 204


@printer.route("/queued-jobs", methods=["GET"])
@check_logged
def get_queued_jobs():
    jobs = PrinterService.get_queued_jobs()
    for j in jobs:
        del j["path"]
    return {
        "jobs": jobs
    }


@printer.route("/printed-jobs", methods=["GET"])
@check_logged
def get_printed_jobs():
    jobs = PrinterService.get_printed_jobs()
    for j in jobs:
        del j["path"]
    return {
        "jobs": jobs
    }


@printer.route("/submit", methods=["POST"])
@check_logged
def submit():
    if "copies" not in request.form:
        return {"error": "copies"}, 400
    copies = int(request.form["copies"])
    if copies < 1 or copies > 100:
        return {"error": "copies"}, 400

    if "print_file" not in request.files:
        return {"error": "print_file"}, 400
    file = request.files["print_file"]
    if file is None or not allowed_file(file.filename):
        return {"error": "print_file"}, 400

    job = PrinterService.add_job_to_queue(file, 8)
    del job["path"]
    return {"job": job}, 201
