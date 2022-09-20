import base64
import cv2
import json
import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo

# Flask Server Backend
app = Flask(__name__)

# save model.h5
model = tf.keras.Sequential([
    tf.keras.layers.Dense(5, input_shape=(784,)),
    tf.keras.layers.Softmax()
])
model.save('/home/phuongpt/dev/faceId/models/my_h5_model.h5')

# Database
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

# Start Backend
if __name__ == '__main__':
    app.run(debug=True)


# Router
@app.route("/")
def hello():
    return "Welcome to Python Flask!"


@app.route('/api/v1/register', methods=['POST'])
def signUp():
    try:
        _json = json.loads(request.data)
        _name = _json['name']
        _username = _json['username']
        _password = _json['password']

        hash_password = generate_password_hash(_password)

        mongo.db.users.insert_one({
            'name': _name,
            'username': _username,
            'password': hash_password
        })

        res = jsonify({'message': 'User added successfully'})
        res.status_code = 201

        return res
    except Exception as error:

        res = jsonify({'message': 'Bad request', 'content': str(error)})
        res.status_code = 400

        return res


@app.route("/api/v1/training", methods=['POST'])
def trainingFace():
    try:
        base64_string_array = json.loads(request.data)['file']
        img = []
        for i in range(len(base64_string_array)):

            image_string = base64.b64decode(base64_string_array[i])
            # print(image_string)

            jpg_as_np = np.frombuffer(image_string, dtype=np.uint8)
            # print(jpg_as_np)

            img.append(cv2.imdecode(jpg_as_np, flags=0))
            print(img)
            cv2.imwrite(f'color_img{i}.jpg', img[i])

            # im = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
            # # print(im)
            # im = im.reshape(784)
            # # print(im)
            #
            # loaded_model = tf.keras.models.load_model('/home/phuongpt/dev/faceId/models/my_h5_model.h5')
            # predict_x = loaded_model.predict(np.array([im]))
            # print(f'predict = {predict_x}, type: {type(predict_x)}')
            #
            # classes_x = np.argmax(predict_x, axis=1)

        # print(img)
        return jsonify({'message': 'Received'})
    except Exception as error:

        res = jsonify({'message': 'Bad request', 'content': str(error)})
        res.status_code = 400

        return res


@app.route('/api/v1/loginByAccount', methods=['POST'])
def signInByAccount():
    try:
        _json = json.loads(request.data)
        username = _json['username']
        password = _json['password']

        if username and password:
            user = mongo.db.users.find_one({'username': username})
            if user is None:
                return {'message': 'User not found'}
            isMatch = check_password_hash(user['password'], password)
            if isMatch is False:
                return {'message': 'Username or password is not correct'}

        res = jsonify({'message': 'Login successfully', 'name': user['name']})
        res.status_code = 200

        return res
    except Exception as error:

        res = jsonify({'message': 'Bad request', 'content': str(error)})
        res.status_code = 400

        return res


@app.route('/api/v1/loginByFace', methods=['POST'])
def signInByFace():
    pass
