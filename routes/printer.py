import os
from flask import Blueprint, render_template, request, redirect
from dotenv import load_dotenv
from bcrypt import checkpw

load_dotenv()

printer = Blueprint("printer", __name__, template_folder="../templates")
SERVER_LOCAL_IP = '192.168.178.69'
COD_MAC = os.environ.get("COD_MAC")


def wake_on_lan():
    # Lanciare pacchetto
    os.system('wakeonlan {} > /dev/null'.format(COD_MAC))
    # TODO Chiamare qui copy_file_to server? Bisogna aspettarere che si accenda il server.

def copy_file_to_server(file_path):
    os.system('scp {} cod@{}:/home/cod/to_print > /dev/null'.format(file_path, SERVER_LOCAL_IP))


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
        file_save_path = "./tmp/" +file.filename
        file.save(file_save_path)
        print(password, copies, file)
        command = 'timeout 0.2s ping {} -c 1 > /dev/null'.format(SERVER_LOCAL_IP)
        ping_res = os.system(command)
        if ping_res == 0:
            copy_file_to_server(file_save_path)
        else:
            wake_on_lan()
    else:
        print("Password sbagliata")
    return redirect("/printer")
