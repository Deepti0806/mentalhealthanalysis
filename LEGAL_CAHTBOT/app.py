from flask import Blueprint, Flask, render_template, request
import google.generativeai as genai
import sqlite3
import csv
import os

def create_legal_chatbot_app():
    app = Blueprint('legal_chatbot', __name__, template_folder='templates', static_folder='static')

    # Configure Gemini AI
    genai.configure(api_key='AIzaSyCaz-8RhG6tW1SuLq5L_QINLTm9neK9dX0')
    gemini_model = genai.GenerativeModel('gemini-pro')
    chat = gemini_model.start_chat(history=[])

    chat_history = []

    # Ensure database table exists
    def init_db():
        with sqlite3.connect('user_data.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS user (
                                name TEXT,
                                password TEXT,
                                mobile TEXT,
                                email TEXT
                            )""")

    init_db()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/home')
    def home():
        return render_template('userlog.html')

    @app.route('/userlog', methods=['GET', 'POST'])
    def userlog():
        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            with sqlite3.connect('user_data.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM user WHERE name=? AND password=?", (name, password))
                result = cursor.fetchone()

            if result:
                return render_template('userlog.html')
            else:
                return render_template('index.html', msg='Sorry, Incorrect Credentials Provided, Try Again')

        return render_template('index.html')

    @app.route('/userreg', methods=['GET', 'POST'])
    def userreg():
        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            mobile = request.form['phone']
            email = request.form['email']

            with sqlite3.connect('user_data.db') as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (name, password, mobile, email))

            return render_template('index.html', msg='Successfully Registered')

        return render_template('index.html')

    @app.route('/analyse', methods=['GET', 'POST'])
    def analyse():
        if request.method == 'POST':
            user_input = request.form['query']

            # Get response from Gemini AI model
            gemini_response = chat.send_message(user_input)
            data = gemini_response.text
            result = [row for row in data.split('*') if row.strip() != '']

            chat_history.append([user_input, result])

            # Lawyer search logic
            lawyer_name = None
            lawyer_link = None
            try:
                with open('lowyer.csv', 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    header = next(reader)
                    for row in reader:
                        if row[1] in user_input:
                            lawyer_name = row[0]
                            lawyer_link = row[2]
                            break

                return render_template('userlog.html', status="Sever", chat_history=chat_history, name=lawyer_name, Link=lawyer_link)
            except Exception as e:
                print(f"Error loading lawyer info: {e}")
                return render_template('userlog.html', chat_history=chat_history)

        return render_template('userlog.html')

    @app.route('/logout')
    def logout():
        return render_template('index.html')

    return app

# Optional: for standalone run
if __name__ == "__main__":
    flask_app = Flask(__name__)
    flask_app.register_blueprint(create_legal_chatbot_app())
    flask_app.run(debug=True)
