from flask import Flask, render_template,request
from helper import getMean
import imageio.v3 as iio
import time
import pickle
import sklearn
import numpy as np
app = Flask(__name__)


loaded_model = pickle.load(open('model.sav', 'rb'))
# two decorators, same function
@app.route('/')
@app.route('/index.html')
def index():

    return "home"




@app.route('/api/v1/')
def apiv1():
    start=time.time()
    args = request.args
    id = args.get('id')
    token=args.get('token')
    baseURL="https://firebasestorage.googleapis.com/v0/b/fluttertest-24277.appspot.com/o/images%2F"+id+"?alt=media&token="+token
    return baseURL
    img = iio.imread(baseURL)
    output=np.array(getMean(img))
    idx = loaded_model.predict(output.reshape(1,2))
    results=["Anemia","Non Anemia"]
    end=time.time()
    return results[idx[0]]



if __name__ == '__main__':
    app.run(debug=True)
