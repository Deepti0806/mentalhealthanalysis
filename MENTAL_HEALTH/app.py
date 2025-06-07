from flask import Blueprint, Flask, render_template, request
import pandas as pd
import pickle
import tensorflow as tf
import numpy as np
import sqlite3
import requests
import os
import time
import telepot
from typing import Tuple

model3 = pickle.load(open("0-3.sav", "rb"))
model11 = pickle.load(open("4-11.sav", "rb"))
MODEL_PATH = 'image_model.tflite'

def get_interpreter(model_path: str) -> Tuple:
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return interpreter, input_details, output_details

def predict_image(image_path: str) -> int:
    interpreter, input_details, output_details = get_interpreter(MODEL_PATH)
    input_shape = input_details[0]['shape']
    img = tf.io.read_file(image_path)
    img = tf.io.decode_image(img, channels=3)
    img = tf.image.resize(img, (input_shape[1], input_shape[2]))
    img = tf.expand_dims(img, axis=0)
    img = tf.cast(img, dtype=tf.uint8)
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return int(np.argmax(np.squeeze(output_data)))

def create_mental_health_app():
    mental_app = Blueprint('mental_health', __name__, template_folder='templates', static_folder='static')

    @mental_app.route('/')
    @mental_app.route('/home')
    @mental_app.route('/logout')
    def home():
        return render_template('index.html')

    @mental_app.route('/sd')
    def sad():
        return render_template('sad.html')

    @mental_app.route('/hp')
    def happy():
        return render_template('happy.html')

    @mental_app.route('/about')
    def about():
        return render_template('about.html')

    @mental_app.route('/userlog', methods=['GET', 'POST'])
    def userlog():
        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            with sqlite3.connect('user_data.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT email FROM user WHERE name=? AND password=?", (name, password))
                result = cursor.fetchone()
            if result:
                with open('session.txt', 'w') as f:
                    f.write(result[0])
                return render_template('index1.html')
            return render_template('index.html', msg='Incorrect credentials, try again.')
        return render_template('index.html')

    @mental_app.route('/userreg', methods=['GET', 'POST'])
    def userreg():
        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            mobile = request.form['phone']
            email = request.form['email']
            with sqlite3.connect('user_data.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS user (name TEXT, password TEXT, mobile TEXT, email TEXT)""")
                cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (name, password, mobile, email))
            return render_template('index.html', msg='Successfully Registered')
        return render_template('index.html')

    @mental_app.route('/adminlog', methods=['GET', 'POST'])
    def adminlog():
        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            with sqlite3.connect('user_data.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM admin WHERE name=? AND password=?", (name, password))
                result = cursor.fetchone()
            if result:
                return render_template('home.html')
            return render_template('index.html', msg='Incorrect admin credentials.')
        return render_template('index.html')

    @mental_app.route('/adminreg', methods=['GET', 'POST'])
    def adminreg():
        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            mobile = request.form['phone']
            email = request.form['email']
            with sqlite3.connect('user_data.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS admin (name TEXT, password TEXT, mobile TEXT, email TEXT)""")
                cursor.execute("INSERT INTO admin VALUES (?, ?, ?, ?)", (name, password, mobile, email))
            return render_template('index.html', msg='Admin Registered')
        return render_template('index.html')

    def preprocess_common(df, ethnicity_map, num_ethnicity):
        data = [int(df[f'A{i}']) for i in range(1, 11)]
        data.append(0 if int(df['age']) < 12 else 1)
        data.append(int(df['gender']))
        ethnicity_vector = [0] * num_ethnicity
        if df['etnicity'] in ethnicity_map:
            ethnicity_vector[ethnicity_map[df['etnicity']]] = 1
        data.extend(ethnicity_vector)
        data.append(int(df['work']))
        data.append(int(df['mh']))
        return data

    @mental_app.route('/Three_year', methods=['GET', 'POST'])
    def Three_year():
        if request.method == 'POST':
            df = request.form
            ethnicity_map = {
                'middle eastern': 0, 'White European': 1, 'Hispanic': 2, 'black': 3, 'asian': 4,
                'south asian': 5, 'Native Indian': 6, 'Others': 7, 'Latino': 8, 'mixed': 9, 'Pacifica': 10
            }
            data = preprocess_common(df, ethnicity_map, 11)
            pred = model3.predict([data])[0]
            prediction = 'Normal' if pred == 0 else 'Mental stress'
            return render_template('index1.html', name=df['name'], email=df['email'], prediction=prediction)
        return render_template('index.html')

    @mental_app.route('/Eleven_year', methods=['GET', 'POST'])
    def Eleven_year():
        if request.method == 'POST':
            df = request.form
            ethnicity_map = {
                'Others': 0, 'Middle Eastern': 1, 'Hispanic': 2, 'White-European': 3, 'Black': 4,
                'South Asian': 5, 'Asian': 6, 'Pasifika': 7, 'Turkish': 8
            }
            data = preprocess_common(df, ethnicity_map, 10)
            pred = model11.predict([data])[0]
            prediction = 'Normal' if pred == 0 else 'Mental stress'
            return render_template('index1.html', name=df['name'], email=df['email'], prediction=prediction)
        return render_template('index.html')

    @mental_app.route('/Image', methods=['GET', 'POST'])
    def image_route():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            filename = request.form['filename']
            path = os.path.join('static/test', filename)
            pred = predict_image(path)
            prediction = 'Normal' if pred == 0 else 'Mental stress'
            return render_template('index1.html', name=name, email=email, prediction=prediction)
        return render_template('index.html')

    @mental_app.route('/get')
    def get_bot_response():
        user_text = request.args.get('msg')
        TOKEN = "6289177310:AAFToe1tsH-WATDkDuiO4vUCkgfVqq09RcQ"
        bot = telepot.Bot(TOKEN)
        bot.sendMessage('5700060171', user_text)
        time.sleep(10)
        message = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset=-1").json()
        try:
            reply = message['result'][0]['message']['text']
        except (KeyError, IndexError):
            reply = "No recent response received."
        return reply

    return mental_app

# If you want to run directly
if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(create_mental_health_app())
    app.run(debug=True)
