from flask import Flask, request, render_template, redirect
import os
import socket
from threading import Timer
import hashlib


SERVER_LOCAL_IP = '192.168.178.69'
SERVER_DDNS = 'pontedera.duckdns.org'
PWD_FILE = 'password.txt'
MAC_FILE = 'mac.txt'

global_status = 'DOWN'
right_pwd = ''
mac = ''


app = Flask(__name__)

def set_status_down():
    global global_status
    global_status = 'DOWN'


def wake_on_lan():
    # Lanciare pacchetto
    os.system('wakeonlan {} > /dev/null'.format(mac))
    # Mettere handler che dopo 1 minuto imposta global status a 'DOWN'
    Timer(60, set_status_down).start()
    pass


@app.route('/', methods=['GET'])
def main():
    global global_status
    args = {}
    command = 'timeout 0.2s ping {} -c 1 > /dev/null'.format(SERVER_LOCAL_IP)
    ping_res = os.system(command)
    args['status'] = 'UP' if ping_res == 0 else global_status
    if args['status'] == 'UP' or args['status'] == 'LOADING':
        ip = socket.gethostbyname(SERVER_DDNS)
        args['ip'] = ip
    return render_template('index.html', args=args)


@app.route('/', methods=['POST'])
def login():
    global global_status
    args = {}
    password = request.form['password'].encode()
    password_hash = hashlib.sha256(password).hexdigest()
    if password_hash == right_pwd:
        wake_on_lan()
        ip = socket.gethostbyname(SERVER_DDNS)
        global_status = 'LOADING'
        args['status'] = 'LOADING'
        args['ip'] = ip
        return redirect('/')
    else:
        args['status'] = 'WRONG_PWD'
        return render_template('index.html', args=args)


@app.before_first_request
def initialize():
    global right_pwd, mac
    with open(PWD_FILE, 'r') as f:
        right_pwd = f.readline().strip()
    with open(MAC_FILE, 'r') as f:
        mac = f.readline().strip()


if __name__ == "__main__":
    app.run()
