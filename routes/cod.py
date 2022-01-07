from flask import request, render_template, redirect, Blueprint
import os
import socket
from threading import Timer
import hashlib
import requests


SERVER_LOCAL_IP = '192.168.178.69'
SERVER_DDNS = 'pontedera.duckdns.org'
COD_PWD = os.environ.get("COD_PWD")
COD_MAC = os.environ.get("COD_MAC")

global_status = 'DOWN'


cod = Blueprint("cod", __name__, template_folder="../templates")

# UTILS


def set_status_down():
    global global_status
    global_status = 'DOWN'


def wake_on_lan():
    # Lanciare pacchetto
    os.system('wakeonlan {} > /dev/null'.format(COD_MAC))
    # Mettere handler che dopo 1 minuto imposta global status a 'DOWN'
    Timer(60, set_status_down).start()
    pass


def shutdown_server():
    requests.get("http://" + SERVER_LOCAL_IP + "/shutdown")
    Timer(120, set_status_down).start()


# FLASK ROUTES

@cod.route('', methods=['GET'])
def main():
    global global_status
    args = {}
    command = 'timeout 0.2s ping {} -c 1 > /dev/null'.format(SERVER_LOCAL_IP)
    ping_res = os.system(command)
    args['status'] = 'UP' if ping_res == 0 and global_status != 'SHUTTING DOWN' else global_status
    if args['status'] == 'UP' or args['status'] == 'LOADING':
        ip = socket.gethostbyname(SERVER_DDNS)
        args['ip'] = ip
    return render_template('cod.html', args=args)


@cod.route('', methods=['POST'])
def login():
    global global_status
    args = {}
    password = request.form['password'].encode()
    password_hash = hashlib.sha256(password).hexdigest()
    print("Sto accendendo", password_hash, )
    if password_hash == COD_PWD:
        print("Passord ok")
        wake_on_lan()
        ip = socket.gethostbyname(SERVER_DDNS)
        global_status = 'LOADING'
        args['status'] = 'LOADING'
        args['ip'] = ip
        return redirect('/')
    else:
        args['status'] = 'WRONG_PWD'
        return render_template('cod.html', args=args)


@cod.route("/shutdown", methods=["POST"])
def shutdown():
    global global_status
    try:
        password = request.json['password'].encode()
        password_hash = hashlib.sha256(password).hexdigest()
        if password_hash == COD_PWD:
            shutdown_server()
            global_status = 'SHUTTING DOWN'
            return '', 201
        else:
            return '', 401
    except:
        return '', 400
