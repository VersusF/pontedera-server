from flask import Blueprint, render_template, request, redirect
from dotenv import load_dotenv
from bcrypt import checkpw
import os

load_dotenv()

printer = Blueprint("printer", __name__, template_folder="../templates")


@printer.route("", methods=["GET"])
def main():
    return render_template("printer.html", args={
        "submit_url": "printer/submit"
    })


@printer.route("/submit", methods=["POST"])
def submit():
    password = request.form['password'].encode("utf8")
    pwd_hash = os.getenv("PRINTER_PWD").encode("utf8")
    if checkpw(password, pwd_hash):
        copies = request.form['copies']
        file = request.files['file_path']
        file.save("./tmp/" + file.filename)
        print(password, copies, file)
    else:
        print("Password sbagliata")
    return redirect("/printer")
