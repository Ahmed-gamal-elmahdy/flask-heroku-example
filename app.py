from flask import Flask, render_template
from helper import getMean
import imageio.v3 as iio
app = Flask(__name__)
import time

# two decorators, same function

def index():
    path = "https://firebasestorage.googleapis.com/v0/b/fluttertest-24277.appspot.com/o/imgs%2Fanemia.jpg?alt=media&token=37cc6379-1263-474c-a0c8-ae2fb364a9f3"
    img=iio.imread(path)
    start=time.time()
    g,r=getMean(img)
    end=time.time()
    return str(end-start)


@app.route('/')
@app.route('/index.html')
def home():
    return "hi"

if __name__ == '__main__':
    app.run(debug=True)
