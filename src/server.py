import base64
import cv2
import json
import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, request
from pymongo import MongoClient

# Flask Server Backend
app = Flask(__name__)

# save model.h5
model = tf.keras.Sequential([
    tf.keras.layers.Dense(5, input_shape=(784,)),
    tf.keras.layers.Softmax()
])
model.save('/home/phuongpt/dev/faceId/models/my_h5_model.h5')

# Database
client = MongoClient('localhost:27017')
db = client.myDatabase

# Start Backend
if __name__ == '__main__':
    app.run(debug=True)


# Router
@app.route("/")
def hello():
    return "Welcome to Python Flask!"


@app.route("/getimage", methods=['POST'])
def getImage():
    image = json.loads(request.data)['file']
    image_string = base64.b64decode(image)
    # print(image_string)

    jpg_as_np = np.frombuffer(image_string, dtype=np.uint8)
    # print(jpg_as_np)
    img = cv2.imdecode(jpg_as_np, flags=0)
    # print(img)
    cv2.imwrite('save_image.jpeg', img)

    im = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
    # print(im)
    im = im.reshape(784)
    # print(im)

    loaded_model = tf.keras.models.load_model('/home/phuongpt/dev/faceId/models/my_h5_model.h5')
    predict_x = loaded_model.predict(np.array([im]))
    print(f'predict = {predict_x}, type: {type(predict_x)}')

    classes_x = np.argmax(predict_x, axis=1)

    # status = db.users.insert_one({
    #     'image': img
    # })

    return jsonify({'message': 'Received', 'placement': str(classes_x)})


