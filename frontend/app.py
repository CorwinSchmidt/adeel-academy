from flask import Flask, render_template, redirect, url_for, request, session
from flask_cors import CORS
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '23r23423988a8f8fsw12'
CORS(app=app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    # when post from signup, set userId and role for user
    if request.method == 'POST':
        session["userId"] = request.get_json()['userId']
        print(session["userId"])
        if request.get_json()['role'] == 'teachers':
            session["role"] = "teacher"
        if request.get_json()['role'] == 'students':
            session["role"] = "student"

        return redirect(url_for('dashboard'))


    return render_template('sign-up.html')

@app.route('/log-in', methods=['GET', 'POST'])
def log_in():
    # when post from signup, set userId and role for user
    if request.method == 'POST':
        print(request.get_json()['userId'])
        session["userId"] = request.get_json()['userId']
        print(session["userId"])
        session["role"] = request.get_json()['role']

        print("redirecting to dhasboard")
    

        return redirect(url_for('dashboard'))

    return render_template('log-in.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html', courses=[session["userId"], "Physics", "Math"])


@app.route('/inbox', methods=['GET', 'POST'])
def inbox():
    return render_template('inbox.html', chats = ["Maria", "Joe", "Frank"])

if __name__ == '__main__':
    app.run(port="8000", debug=True)