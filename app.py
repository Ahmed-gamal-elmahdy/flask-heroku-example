from flask import Flask, render_template
from helper import getMean
import imageio.v3 as iio
app = Flask(__name__)
import time

# two decorators, same function
@app.route('/')
@app.route('/index.html')
def index():

    return "home"


@app.route('/api/<string:name>/')
def apitest(name):
    return name
    img = iio.imread(name)
    start = time.time()
    g, r = getMean(img)
    end = time.time()
    return str(end-start)


if __name__ == '__main__':
    app.run(debug=True)
