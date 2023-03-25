<<<<<<< Updated upstream
from flask import Flask, render_template, request
=======
from flask import Flask,request
>>>>>>> Stashed changes
from helper import *
import imageio.v3 as iio
import pickle
import numpy as np
import cv2
from io import BytesIO
app = Flask(__name__)


loaded_model = pickle.load(open('model.sav', 'rb'))
# two decorators, same function


@app.route('/')
@app.route('/index.html')
def index():
    return "home"


@app.route('/api/v1/')
def apiv1():
    args = request.args
    id = args.get('id')
    token = args.get('token')
    baseURL = "https://firebasestorage.googleapis.com/v0/b/fluttertest-24277.appspot.com/o/images%2F" + \
        id+"?alt=media&token="+token
    temp_img = iio.imread(baseURL)
    _, buffer = cv2.imencode(".jpg", temp_img)
    io_buf = BytesIO(buffer)
    decode_img = cv2.imdecode(np.frombuffer(io_buf.getbuffer(), np.uint8), -1)
    output = np.array(get_mean(decode_img))
    idx = loaded_model.predict(output.reshape(1, 2))
    results = ["Anemic", "Not Anemic"]
    return results[int(idx)]


<<<<<<< Updated upstream
=======
@app.route('/api/v2/')
def apiv1():
    args = request.args
    id = args.get('id')
    token=args.get('token')
    uid =args.get('uid')
    baseURL="https://firebasestorage.googleapis.com/v0/b/fluttertest-24277.appspot.com/o/images%2F"+uid+'%2F'+id+"?alt=media&token="+token
    temp_img = iio.imread(baseURL)
    _, buffer = cv2.imencode(".jpg", temp_img)
    io_buf = BytesIO(buffer)
    decode_img = cv2.imdecode(np.frombuffer(io_buf.getbuffer(), np.uint8), -1)
    output = np.array(getMean(decode_img))
    idx = loaded_model.predict(output.reshape(1, 2))
    results = ["Anemic", "Not Anemic"]
    return results[int(idx)]




>>>>>>> Stashed changes
if __name__ == '__main__':
    app.run(debug=True)
