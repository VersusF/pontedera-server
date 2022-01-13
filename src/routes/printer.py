import os
import bcrypt
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
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
    return render_template("printer.html", args={
        "submit_url": "printer/submit"
    })


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


@printer.route("/queued-jobs", methods=["GET"])
@check_logged
def get_queued_jobs():
    jobs = PrinterService.get_queued_jobs()
    return {
        "jobs": jobs
    }


@printer.route("/printed-jobs", methods=["GET"])
@check_logged
def get_printed_jobs():
    jobs = PrinterService.get_printed_jobs()
    return {
        "jobs": jobs
    }


@printer.route("/submit", methods=["POST"])
@check_logged
def submit():
    # TODO: Implement me
    job = PrinterService.add_job_to_queue("filename.pdf", "percorso", 8)
    return {
        "job": job,
    }, 201


# @printer.route("/submit", methods=["POST"])
# def submit():
#     password = request.form["password"].encode("utf8")
#     pwd_hash = os.getenv("PRINTER_PWD").encode("utf8")
#     if checkpw(password, pwd_hash):
#         copies = request.form["copies"]
#         file = request.files["file_path"]
#         if file.filename == "":
#             print("File non selezionato")
#             return redirect("/printer")
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save("./tmp/" + filename)
#             print(password, copies, file)
#             command = "timeout 0.2s ping {} -c 1 > /dev/null".format(SERVER_LOCAL_IP)
#             ping_res = os.system(command)
#             if ping_res == 0:
#                 remote_print(filename, copies)
#             else:
#                 wake_on_lan()
#         else:
#             print("File non in formato PDF")
#     else:
#         print("Password sbagliata")
#     return None, 201
