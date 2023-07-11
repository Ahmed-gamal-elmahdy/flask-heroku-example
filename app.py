
from flask import Flask,request,Response, send_file
from helper import *
import imageio.v3 as iio
import pickle
import numpy as np
import cv2
from io import BytesIO
from tflite_runtime.interpreter import Interpreter

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



@app.route('/api/v2/')
def apiv2():
    args = request.args
    id = args.get('id')
    token=args.get('token')
    uid =args.get('uid')
    baseURL="https://firebasestorage.googleapis.com/v0/b/fluttertest-24277.appspot.com/o/images%2F"+uid+'%2F'+id+"?alt=media&token="+token
    temp_img = iio.imread(baseURL)
    _, buffer = cv2.imencode(".jpg", temp_img)
    io_buf = BytesIO(buffer)
    decode_img = cv2.imdecode(np.frombuffer(io_buf.getbuffer(), np.uint8), -1)
    output = np.array(get_mean(decode_img))
    idx = loaded_model.predict(output.reshape(1, 2))
    results = ["Anemic", "Not Anemic"]
    return results[int(idx)]



def ceil_and_floor_mask(mask):
    mask[mask > 0.5] = np.ceil(mask[mask > 0.5])
    mask[mask <= 0.5] = np.floor(mask[mask <= 0.5])
    return mask

"""Function with tflite"""

def segmentation_tflite(model_path,img):
  img_height=img.shape[0]
  img_width=img.shape[1]
    # Load TFLite model.
  interpreter = Interpreter(model_path=model_path)

  # Allocate memory for the model.
  interpreter.allocate_tensors()

  # Get input and output tensors.
  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()


  img = cv2.resize(img, (256, 256))
  img = img.astype(np.float32) / 255.0


  # Add batch dimension.
  img = np.expand_dims(img, axis=0)

  # Set input tensor.
  interpreter.set_tensor(input_details[0]['index'], img)

  # Run inference.
  interpreter.invoke()

  # Get output tensor.
  output_data = interpreter.get_tensor(output_details[0]['index'])
  pred=np.squeeze(output_data)
  mask=ceil_and_floor_mask(pred)
  img=np.squeeze(img)

  seg0=img[:,:,0]*mask
  seg1=img[:,:,1]*mask
  seg2=img[:,:,2]*mask
  rgb = np.dstack((seg2,seg1,seg0))
  segmented_img = cv2.resize(rgb ,(img_height, img_width))
  return segmented_img



@app.route('/api/v3/')
def apiv3():
    args = request.args
    id = args.get('id')
    token = args.get('token')
    uid = args.get('uid')
    baseURL = "https://firebasestorage.googleapis.com/v0/b/fluttertest-24277.appspot.com/o/images%2F" + uid + '%2F' + id + "?alt=media&token=" + token
    temp_img = iio.imread(baseURL)
    _, buffer = cv2.imencode(".jpg", temp_img)
    io_buf = BytesIO(buffer)
    decode_img = cv2.imdecode(np.frombuffer(io_buf.getbuffer(), np.uint8), -1)
    segmented_img=segmentation_tflite("UNETV1.0.tflite", decode_img)
    output = np.array(get_mean(segmented_img))
    idx = loaded_model.predict(output.reshape(1, 2))
    results = ["Anemic", "Not Anemic"]
    string_result_bytes = results[int(idx)].encode('utf-8')
    # Encode the segmented image as bytes using OpenCV's imencode method
    _, segmented_img_bytes = cv2.imencode('.jpg', segmented_img)
    # Concatenate the image bytes and string result bytes
    response_bytes = segmented_img_bytes.tobytes() + string_result_bytes
    # Create a Flask Response object with the concatenated bytes as the response data
    response = Response(response_bytes, content_type='image/jpeg')
    # Set the content-disposition header to force the browser to download the image instead of displaying it
    response.headers['Content-Disposition'] = 'attachment; filename=image.jpg'
    # Return the Flask Response object
    return response




if __name__ == '__main__':
    app.run(debug=True)
