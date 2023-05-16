from flask import Flask, request, jsonify, render_template, redirect, url_for
import socket
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
# create the flask app
app = Flask(__name__)

# what html should be loaded as the home page when the app loads?
@app.route('/')
def home():
    #return_data()
    return render_template('app_frontend.html')


    #return 'Description entered: {}'.format(a_description)
# define the logic for reading the inputs from the WEB PAGE, 
# running the model, and displaying the prediction
@app.route('/send', methods=['GET','POST'])
def send_data():
    # get the description submitted on the web page
    print("TCP Client Started")
    rcmd = request.form.get('rcmd')
    print(rcmd)
    if rcmd == None:
        rcmd = "TX:NOW"
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 1240  # The port used by the server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(rcmd.encode())
            data = s.recv(1024)
            print(f"Received {data!r}")
    except:
        print("TCP Client Socket Error")
    return redirect(url_for('home'))


@app.route("/data")
def return_data():
    print("TCP Server Started")

    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 1235  # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        try:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:              
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
                    s.close()
                    return render_template('button.html', header_hex_bits=data, payload_hex_bits="00 01 02 03 04")
        except:
            print("timeout or error: process will restart")
            return render_template("no_button.html")


# boilerplate flask app code
if __name__ == "__main__":
    '''scheduler = BackgroundScheduler()
    scheduler.add_job(return_data, "interval", seconds=5)
    scheduler.start()
    '''
    app.run(debug=True)
