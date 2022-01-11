import os
from flask import Blueprint, render_template, request, redirect
from bcrypt import checkpw
from werkzeug.utils import secure_filename
from services import RedisService

printer = Blueprint("printer", __name__, template_folder="../templates")
SERVER_LOCAL_IP = '192.168.178.69'
COD_MAC = os.environ.get("COD_MAC")
ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    """
    Check file type
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def wake_on_lan():
    """
    Launch wake on lan command to wake up print server
    """
    # Lanciare pacchetto
    os.system('wakeonlan {} > /dev/null'.format(COD_MAC))
    # TODO Chiamare qui copy_file_to server? Bisogna aspettarere che si accenda il server.


def remote_print(filename, n_copies):
    """
    Copy file to print to remote host, remove it from local resources
    and start remote host print routine
    """
    os.system('scp {} cod@{}:/home/cod/to_print > /dev/null'.format("./tmp/" + filename, SERVER_LOCAL_IP))
    os.system('rm ./tmp/{} > /dev/null'.format(filename))
    os.system('ssh cod@{} \'lp -n {} /home/cod/to_print/{}\' > /dev/null'.format(SERVER_LOCAL_IP, n_copies, filename))


@printer.route("", methods=["GET"])
def main():
    return render_template("printer.html", args={
        "submit_url": "printer/submit"
    })


@printer.route("/status", methods=["GET"])
def status():
    printer_status = RedisService.get("PRINTER_STATUS")
    return {
        "status": str(printer_status)
    }


@printer.route("/submit", methods=["POST"])
def submit():
    password = request.form['password'].encode("utf8")
    pwd_hash = os.getenv("PRINTER_PWD").encode("utf8")
    if checkpw(password, pwd_hash):
        copies = request.form['copies']
        file = request.files['file_path']
        if file.filename == '':
            print("File non selezionato")
            return redirect("/printer")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save("./tmp/" + filename)
            print(password, copies, file)
            command = 'timeout 0.2s ping {} -c 1 > /dev/null'.format(SERVER_LOCAL_IP)
            ping_res = os.system(command)
            if ping_res == 0:
                remote_print(filename, copies)
            else:
                wake_on_lan()
        else:
            print("File non in formato PDF")
    else:
        print("Password sbagliata")
    return redirect("/printer")
