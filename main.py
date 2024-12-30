import json
from flask import Flask, render_template, redirect, url_for
import serial
import time
import fputils as fp


app = Flask(__name__)
users = {}

def findnextid():
    i = 0
    while i in users:
        i += 1
    return i

def save_users():
    with open('users.json', 'w') as f:
        json.dump(users, f)

def load_users():
    global users
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except:
        users = {}

@app.route('/')
def home():
    if fp.init():
        fp.led(fp.LED_ON, 7)

    return render_template('index.html', message=users)

@app.route('/empty')
def empty():
    if fp.init():
        global users
        users = {}
        save_users()
        fp.empty_database()

        fp.led(fp.LED_BREATHING, fp.LED_YELLOW)
        return render_template('index.html', message='Database emptied')
    else:
        return render_template('index.html', message='Initialization failed')

@app.route('/enroll')
def enroll():
    if fp.init():
        fp.read_fingerprint(1)
        fp.read_fingerprint(2)
        fp.create_model()
        id = findnextid()
        fp.store_model(id)
        users[id] = {'id': id, 'name': None, 'age': None}
        save_users()
        fp.led(fp.LED_BREATHING, fp.LED_BLUE)
        return render_template('index.html', message='Fingerprint enrolled and stored at location ' + str(id))
    else:
        return render_template('index.html', message='Initialization failed')

@app.route('/read')
def read():
    if fp.init():
        fp.read_fingerprint(1)
        ret = fp.finger_search()

        if ret[0] == fp.RET_OK and ret[1] in users:
            
            infos = users[ret[1]]
            fp.led(fp.LED_BREATHING, fp.LED_GREEN)
            return render_template('index.html', message='Fingerprint found. Infos: ' + str(infos))
        else:
            fp.led(fp.LED_BREATHING, fp.LED_RED)
            return render_template('index.html', message='Fingerprint not found. Infos: ' + str(ret))
    else:
        return render_template('index.html', message='Initialization failed')

if __name__ == "__main__":
    # if fp.init():
    #     fp.empty_database()
    #     fp.led(fp.LED_BREATHING, 5)
    
    if fp.arduino == None:
        fp.arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)  # Replace 'COM3' with your Arduino's port
        time.sleep(2)
        fp.init()
        fp.led(fp.LED_BREATHING, fp.LED_WHITE)


    load_users()
    if users == {}:
        fp.led(fp.LED_BREATHING, fp.LED_YELLOW)
    else:
        fp.led(fp.LED_BREATHING, fp.LED_WHITE)


    app.run(debug=False)
