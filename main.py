from flask import Flask, render_template, redirect, url_for
import serial
import time
import fputils as fp


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/empty')
def empty():
    if fp.init():
        fp.empty_database()
        fp.led(fp.LED_BREATHING, 5)
        return "Database emptied"
    else:
        return "Initialization failed"

@app.route('/enroll')
def enroll():
    if fp.init():
        fp.read_fingerprint(1)
        fp.read_fingerprint(2)
        fp.create_model()
        fp.store_model(10)
        return "Fingerprint enrolled and stored"
    else:
        return "Initialization failed"

@app.route('/read')
def read():
    if fp.init():
        fp.read_fingerprint(1)
        ret = fp.finger_search()
        return f"Fingerprint read: {ret}"
    else:
        return "Initialization failed"

if __name__ == "__main__":
    # if fp.init():
    #     fp.empty_database()
    #     fp.led(fp.LED_BREATHING, 5)

    app.run(debug=False)
