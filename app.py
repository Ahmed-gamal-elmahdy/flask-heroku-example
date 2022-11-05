from flask import Flask, render_template,request
from helper import getMean
import imageio.v3 as iio
app = Flask(__name__)
import time

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
def apiv1():
    args = request.args
    url = args.get('url')
    return str(url)



if __name__ == '__main__':
    app.run(debug=True)
