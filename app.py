
# from flask import Flask, render_template, request, redirect, url_for, session
# import sqlite3
# import os
# import pickle
# import numpy as np

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# # Ensure the database and tables are initialized
# def init_db():
#     if not os.path.exists('database.db'):
#         conn = sqlite3.connect('database.db')
#         cursor = conn.cursor()
#         cursor.execute('''CREATE TABLE users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             email TEXT UNIQUE NOT NULL,
#             password TEXT NOT NULL
#         )''')
#         cursor.execute('''CREATE TABLE predictions (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_email TEXT,
#             val1 REAL, val2 REAL, val3 REAL,
#             val4 REAL, val5 REAL, val6 REAL,
#             val7 REAL, val8 REAL, val9 REAL,
#             result TEXT
#         )''')
#         conn.commit()
#         conn.close()

# init_db()

# # Load the trained model
# model = pickle.load(open('model.pkl', 'rb'))

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
#         conn = sqlite3.connect('database.db')
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
#         conn.commit()
#         conn.close()
#         return redirect(url_for('login'))
#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email'].strip()
#         password = request.form['password'].strip()
        
#         conn = sqlite3.connect('database.db')
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
#         user = cursor.fetchone()
#         conn.close()
        
#         if user:
#             session['email'] = email
#             return redirect(url_for('predict'))
#         else:
#             return "Invalid Credentials"  # You can replace with a styled error message
#     return render_template('login.html')


# @app.route('/logout')
# def logout():
#     session.pop('email', None)
#     return redirect(url_for('home'))
# @app.route('/predict', methods=['GET', 'POST'])
# def predict():
#     inputs = [
#     float(request.form.get('soil_moisture', 0)),
#     float(request.form.get('leaf_temp', 0)),
#     float(request.form.get('air_temp', 0)),
#     float(request.form.get('humidity', 0)),
#     float(request.form.get('light', 0)),
#     float(request.form.get('soil_ph', 0)),
#     float(request.form.get('ec', 0)),
#     float(request.form.get('stem_diameter', 0)),
#     float(request.form.get('leaf_thickness', 0))
# ]

#     if request.method == 'POST':
#         inputs = [float(request.form.get(f'val{i}', 0)) for i in range(1, 10)]
#         input_array = np.array([inputs])
#         prediction = model.predict(input_array)[0]
#         levels = ['Healthy', 'Mild Stress', 'Moderate Stress', 'Severe Stress']
#         result = levels[int(prediction)] if int(prediction) < len(levels) else 'Unknown'

#         conn = sqlite3.connect('database.db')
#         cursor = conn.cursor()
#         cursor.execute('''INSERT INTO predictions (user_email, val1, val2, val3, val4, val5, val6, val7, val8, val9, result)
#                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
#                           (session.get('email', 'guest'), *inputs, result))
#         conn.commit()
#         conn.close()

#         return render_template('result.html', result=result)
#     return render_template('predict.html')

# if os.path.exists('database.db'):
#     os.remove('database.db')
# init_db()

# @app.route('/precautions')
# def precautions():
#     return render_template('precautions.html')

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# if os.path.exists('database.db'):
#     os.remove('database.db')

# Ensure the database and tables are initialized
def init_db():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')
        cursor.execute('''CREATE TABLE predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            soil_moisture REAL,
            leaf_temp REAL,
            air_temp REAL,
            humidity REAL,
            light REAL,
            soil_ph REAL,
            ec REAL,
            stem_diameter REAL,
            leaf_thickness REAL,
            result TEXT
        )''')
        conn.commit()
        conn.close()

init_db()

# Load the trained model
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['email'] = email
            return redirect(url_for('predict'))
        else:
            return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            inputs = [
                float(request.form.get('soil_moisture', 0)),
                float(request.form.get('leaf_temp', 0)),
                float(request.form.get('air_temp', 0)),
                float(request.form.get('humidity', 0)),
                float(request.form.get('light', 0)),
                float(request.form.get('soil_ph', 0)),
                float(request.form.get('ec', 0)),
                float(request.form.get('stem_diameter', 0)),
                float(request.form.get('leaf_thickness', 0))
            ]
            input_array = np.array([inputs])
            prediction = model.predict(input_array)[0]
            levels = ['Severe Stress', 'Moderate Stress', 'Mild Stress', 'Healthy']

            result = levels[int(prediction)] if int(prediction) < len(levels) else 'Unknown'

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO predictions (
                user_email, soil_moisture, leaf_temp, air_temp, humidity,
                light, soil_ph, ec, stem_diameter, leaf_thickness, result
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (session.get('email', 'guest'), *inputs, result))
            conn.commit()
            conn.close()

            return render_template('result.html', result=result, inputs=inputs)
        except Exception as e:
            return f"Error during prediction: {str(e)}"
    return render_template('predict.html')

@app.route('/precautions')
def precautions():
    return render_template('precautions.html')

if __name__ == '__main__':
    app.run(debug=True)
