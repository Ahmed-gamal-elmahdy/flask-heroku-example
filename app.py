from flask import Flask, render_template,request
from helper import getMean
import imageio.v3 as iio
import time
import pickle
import sklearn
app = Flask(__name__)

loaded_model = pickle.load(open('model.sav', 'rb'))
# two decorators, same function
@app.route('/')
@app.route('/index.html')
def index():

    return "home"



def apitest(name):
    return str(name)
    img = iio.imread(name)
    start = time.time()
    g, r = getMean(img)
    end = time.time()
    return str(end-start)


@app.route('/<string:name>/')
def apiroute(name):
    return name

@app.route('/api/')
def api():
    args = request.args
    id = args.get('id')
    token=args.get('token')
    baseURL="https://firebasestorage.googleapis.com/v0/b/fluttertest-24277.appspot.com/o/images%2F"+str(id)+"?alt=media&token="+str(token)
    return baseURL

@app.route('/api/v1/')
def apiv1():
    args = request.args
    id = args.get('id')
    token=args.get('token')
    baseURL="https://firebasestorage.googleapis.com/v0/b/fluttertest-24277.appspot.com/o/imgs%2F"+id+"?alt=media&token="+token
    img = iio.imread(baseURL)
    start = time.time()
    idx = loaded_model.predict(getMean(img).reshape(1,-1))
    results=["Non","Anemia"]
    end = time.time()
    return str(end - start)+"result"+results[idx]



if __name__ == '__main__':
    app.run(debug=True)
