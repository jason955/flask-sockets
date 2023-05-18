from flask import Flask, request, jsonify, render_template, redirect, url_for
import socket
import datetime
import threading

#THREADING TCP SERVER SHARED GLOBAL VAR 
global hex_data
hex_data = None
#THREADING TCP SERVER SHARED GLOBAL VAR

SERVER_HOST = "127.0.0.1"  # The server's hostname or IP address
SERVER_PORT = 1240  # The port used by the server

# TCP Server running on a thread continously
# update global var hex_data and respond with 'Data Received'
def tcp_server():
    global hex_data
    print("TCP Server Started")
    while True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen()
        conn, addr = server_socket.accept()
        hex_data = conn.recv(1024)
        conn.sendall(b"Data Received")
        print(hex_data)
    server_socket.close()
    if data:
        print("Received data: " + str(data))

tcp_server_t = threading.Thread(target=tcp_server, name="Alarm")
tcp_server_t.start()


CLIENT_HOST = "127.0.0.1"  # The client's hostname or IP address
CLIENT_PORT = 1235  # The port used by the client

def tcp_client(cmd, host, port):
    print("TCP Client Started")
    print(f'{cmd} about to be sent')
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((CLIENT_HOST, CLIENT_PORT))
            s.sendall(cmd.encode())
            data = s.recv(1024)
            print(f"Received {data!r}")
    except:
        print("TCP Client Socket Error")
################################################################
### Flask App Start
################################################################




# create the flask app
app = Flask(__name__)

# Base route for 127.0.0.1:5000
@app.route('/')
def home():
    return render_template('app_frontend.html')




#Send replay from button press
@app.route('/send_cmd_line', methods=['GET','POST'])
def send_cmd_line():
    # get the description submitted on the web page
    if 1:
        cmdl = request.form.get('cmdl')
        rcmd = "TX:NOW"
        tcp_client(cmdl, CLIENT_HOST, CLIENT_PORT)
    else:
        print("Not in CMD Line TX Mode")
    return redirect(url_for('home'))

#Send replay from button press
@app.route('/send_replay', methods=['GET','POST'])
def send_replay():
    rcmd = "TX:NOW"
    tcp_client(rcmd, CLIENT_HOST, CLIENT_PORT)
    return redirect(url_for('home'))

@app.route('/send_start', methods=['GET','POST'])
def send_start():
    rcmd = "START"
    tcp_client(rcmd, CLIENT_HOST, CLIENT_PORT)
    return redirect(url_for('home'))

@app.route('/set_freq', methods=['GET','POST'])
def send_freq():
    rcmd = "FREQ"
    tcp_client(rcmd, CLIENT_HOST, CLIENT_PORT)
    return redirect(url_for('home'))

@app.route('/set_sf', methods=['GET','POST'])
def send_sf():
    rcmd = "SF"
    tcp_client(rcmd, CLIENT_HOST, CLIENT_PORT)
    return redirect(url_for('home'))

@app.route('/set_xx', methods=['GET','POST'])
def send_xx():
    rcmd = "XX"
    tcp_client(rcmd, CLIENT_HOST, CLIENT_PORT)
    return redirect(url_for('home'))

@app.route('/set_xxx', methods=['GET','POST'])
def send_xxx():
    rcmd = "XXX"
    tcp_client(rcmd, CLIENT_HOST, CLIENT_PORT)
    return redirect(url_for('home'))    

@app.route("/data")
def return_data():
    global hex_data
    data = hex_data
    if hex_data != None:
        print(data)
        hex_data = None
        return render_template('button.html', header_hex_bits=data, payload_hex_bits="00 01 02 03 04") 
    else:
        print("No data")
        return render_template("no_button.html")

# boilerplate flask app code
if __name__ == "__main__":
    app.run()
