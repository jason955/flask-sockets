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
    a_description = request.form.get('description')
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65433  # The port used by the server

    #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s.connect((HOST, PORT))
        #s.sendall(b"Hello, world")
        #data = s.recv(1024)

    #print(f"Received {data!r}")
    return redirect(url_for('home'))

    #return 'Description entered: {}'.format(a_description)

@app.route("/data")
def return_data():
    print("here")
    a_description = "JASON"

    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 1235  # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        s.bind((HOST, PORT))
        s.listen()
        try:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:              
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
                    s.close()
                    return render_template('button.html', hex_bits=data)
        except:
            print("timeout")
            return render_template("no_button.html")
#@app.route('/api/background-task', methods=['GET'])
#def background_task():
#    new_thread = NewThreadedTask()
#    new_thread.start()
    # optionally wait for task to complete
#    new_thread.join()
#    return {'status': 'ok'}, 200
#https://www.pythonforthelab.com/blog/handling-and-sharing-data-between-threads/
#https://unbiased-coder.com/python-flask-multithreading/
#@app.route('/prediction', methods=['GET', 'POST'])
#def prediction():
#    if request.method == 'POST':
#        prediction_data = request.json
#        print(prediction_data)
#    return jsonify({'result': prediction_data})

# boilerplate flask app code
if __name__ == "__main__":
    '''scheduler = BackgroundScheduler()
    scheduler.add_job(return_data, "interval", seconds=5)
    scheduler.start()
    '''
    app.run(debug=True)
