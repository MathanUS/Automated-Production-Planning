from flask import Flask, jsonify, render_template, request, redirect, url_for, session, g
import sqlite3
import os
from backend import *

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)

# Function to get the SQLite connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('Industry.db')
        db.row_factory = sqlite3.Row
    return db

# Function to close the SQLite connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_check', methods=['POST'])
def login_check():
    mail = request.form['mail']
    password = request.form['password']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT mail, password FROM CUSTOMER WHERE mail = ? and password = ?", (mail, password))
    row = cursor.fetchone()
    conn.close()
    if row:
        session['logged_in'] = True
        session['user_mail'] = mail
        return redirect(url_for('input'))
    else:
        return redirect(url_for('login'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    mail = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT mail FROM CUSTOMER WHERE mail = ?", (mail,))
    existing_user = cursor.fetchone()
    if existing_user:
        conn.close()
        return redirect(url_for('login'))
    else:
        cursor.execute("INSERT INTO CUSTOMER (name, mail, phone, password) VALUES (?, ?, ?, ?)", (name, mail, phone, password))
        conn.commit()
        conn.close()
        return redirect(url_for('input'))

@app.route('/input', methods=['GET', 'POST'])
def input():
    return render_template('input.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        user_mail = session['user_mail']
        taskId = int(request.form['taskId'])
        machineId = int(request.form['machineId'])
        duration = int(request.form['duration'])

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM CUSTOMER WHERE mail = ?", (user_mail,))
        user_id = cursor.fetchone()[0]
        
        cursor.execute('''INSERT INTO TASK (taskId, machineId, duration, user_id) VALUES (?, ?, ?, ?);''',
                    (taskId, machineId, duration, user_id))
        conn.commit()

        return redirect(url_for('input'))

@app.route('/output', methods=['GET'])
def output():
    user_mail = session['user_mail']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM CUSTOMER WHERE mail = ?", (user_mail,))
    user_id = cursor.fetchone()[0]
    conn.commit()
    output_data = main(user_id)  # Fetch output from backend
    return render_template('output.html', output=output_data)

@app.route('/display', methods=['GET'])
def display():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    user_mail = session['user_mail']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT taskId, machineId, duration FROM TASK WHERE user_id = (SELECT id FROM CUSTOMER WHERE mail = ?)", (user_mail,))
    tasks = cursor.fetchall()
    conn.close()

    return render_template('display.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
