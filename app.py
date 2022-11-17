from flask import Flask, render_template,request
from helper import *
import imageio.v3 as iio
import pickle
import sklearn
import numpy as np
import cv2
import time
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
    token=args.get('token')
    baseURL="https://firebasestorage.googleapis.com/v0/b/fluttertest-24277.appspot.com/o/images%2F"+id+"?alt=media&token="+token
    temp_img = iio.imread(baseURL)
    path = str(time.time()) + "temp.jpeg"
    cv2.imwrite(path, temp_img)
    img = cv2.imread(path)
    output=np.array(getMean(img))
    idx = loaded_model.predict(output.reshape(1,2))
    results=["Anemic","Not Anemic"]
    return results[idx[0]]






if __name__ == '__main__':
    app.run(debug=True)
