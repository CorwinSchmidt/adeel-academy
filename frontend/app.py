from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from requests.api import get
from flask_cors import CORS
from wtforms import Form, StringField, PasswordField, validators, SubmitField, RadioField
import requests
import json
from req import req


app = Flask(__name__)
app.config['SECRET_KEY'] = '23r23423988a8f8fsw12'
CORS(app=app)


# forms
class SignUp(Form):
    name = StringField('Name', validators=[validators.DataRequired()])
    email = StringField('Email Address', validators=[validators.DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired()])
    role = RadioField('Role', choices=[('Teacher'),('Student')])
    submit = SubmitField('Sign Up')
class LogIn(Form):
    email = StringField('Email Address', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Log In')

# request template


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    # init form
    form = SignUp(request.form)

    # on post
    if request.method == 'POST' and form.validate():
        print("getting form")
        name = form.name.data
        email = form.email.data
        password = form.password.data
        option = form.role.data

        data = {
            'email': email,
            'password': password,
        }

        resp = requests.post("http://127.0.0.1:5000/logins", json=data) # this works

        print(resp.status_code, resp.reason, resp.json )

        if resp.status_code == 200:
            print("good response")
            # get loginId from json response
            json_data = json.loads(resp.text)
            session["loginId"] = json_data["loginId"]

            data = {
                    'name': name,
                    'email': email,
                    'connected': "true",
                    'loginId': session["loginId"],
                }

            # create based on teacher or student
            if option == "Teacher":
                session["role"] = "teacher"
                resp = requests.post("http://127.0.0.1:5000/teachers", json=data)
                print("teacher")
            else:
                session["role"] = "student"
                resp = requests.post("http://127.0.0.1:5000/students", json=data)
                print("student")
            
            # if new status code is good, redirect, or show error
            if resp.status_code == 200:
                print(session["loginId"])

                return redirect(url_for('dashboard'))
            else:
                flash("There was an error creating your account. Please try again later.")
                
        else:
            flash("There was an error creating your account. Please try again later.")


        # return redirect(url_for('log-in'))
    return render_template('sign-up.html', form=form)



@app.route('/log-in', methods=['GET', 'POST'])
def log_in():

    # when post from signup, set userId and role for user
    form = LogIn(request.form)
    if request.method == 'POST' and form.validate():
        print("getting form")
        email = form.email.data
        password = form.password.data

        data = {
            'email': email,
            'password': password,
        }

        resp = requests.post("http://127.0.0.1:5000/logincheck", json=data)

        print(resp.status_code, resp.reason, resp.json )

        if resp.status_code == 200:
            # get loginId from json response
            json_data = json.loads(resp.text)
            session["loginId"] = json_data["loginId"]
            session["role"] = json_data["role"]
            return redirect(url_for('dashboard'))
        else:
            flash("There was an error logging into your account. Please try again later.")



    return render_template('log-in.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))

    courses = []

    # get courses based on role
    if session["role"] == "student":

        # get studentId by login and set session
        request = req("get", "studentbyloginid", id=session["loginId"])
        try:
            session["studentId"] = request["studentId"]
        except Exception as e:
            print(e)
        
        # get courses
        request = req("get", "studentcourses", id=session["studentId"])
        for i in request:
            courses_req = req("get", "courses", id=i["courseId"])
            courses.append(courses_req)
    else:

        # get teacherId by login and set session
        request = req("get", "teacherbyloginid", id=session["loginId"])
        try:
            session["teacherId"] = request["teacherId"]
        except Exception as e:
            print(e)
        
        # get courses
        request = req("get", "teachercourses", id=session["teacherId"])
        for i in request:
            courses_req = req("get", "courses", id=i["courseId"])
            courses.append(courses_req)
    
    print(courses)

    return render_template('dashboard.html', courses=courses)

# Displays a static contact page for support
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Displays a user's chats and the messages therein
@app.route('/inbox', methods=['GET', 'POST'])
def inbox():
    return render_template('inbox.html', chats = ["Maria", "Joe", "Frank"])

# Displays all courses, along with a search bar + allows teachers to create a course
@app.route('/all-courses', methods=['GET', 'POST'])
def courses():
    return render_template('all-courses.html')

# Displays a single course and its information
@app.route('/course/<courseId>', methods=['GET', 'POST'])
def course(courseId):
    # Get course by id, pass to render template

    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))

    modules = []
    assignments = []
    name = ""
    description=""

    print(session["role"])
    # get courses based on role
    if session["role"] == "student":
        print("fdsa")
        # get studentId by login and set session
        # request = req("get", "course", id=courseId)

        # get courses
    else:
        print("fdsa")
        # get studentId by login and set session
        print(courseId)
        request = req("get", "courses", id=courseId)
        name = request["name"]
        description = request["description"]
        print("lok", description)
        modules = request["modules"]
        # assignments = request["assignments"] # not added yet

        print(request)
        # get courses


  


    # This is temporary, for design purposes:
    return render_template('course.html', courseId=courseId, courseName= name, courseDesc=description, 
            courseModules=["module1", "module2", "module3"], courseAssignments=['assignment1','assignment2','assignment3'])

# Displays a student's assignments
@app.route('/student-assignments', methods=['GET', 'POST'])
def studentAssignments():
    return render_template('student-assignments.html')

# Displays the results of a search conducted from the 
@app.route('/results', methods=['GET', 'POST'])
def results():
    # need to get users and courses that match input in search bar
    return render_template('search-results.html', users=['user 1', 'user 2'], courses=['course 1', 'course 2'])

# Logs the user out
@app.route('/log-out', methods=['GET', 'POST'])
def logOut():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port="8000", debug=True)