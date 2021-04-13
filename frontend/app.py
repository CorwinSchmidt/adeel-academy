from typing import NoReturn
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, Response
from requests.api import get
from requests.models import RequestHooksMixin
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

@app.route('/')
def index():
    if session.get("loginId") is not None:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    if session.get("loginId") is not None:
        return redirect(url_for('dashboard'))

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

    if session.get("loginId") is not None:
        return redirect(url_for('dashboard'))

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
        
        # get courses by studentId
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
    
    numCourses = len(courses)

    return render_template('dashboard.html', courses=courses, numCourses=numCourses)

# Displays a static contact page for support
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Displays a user's chats
@app.route('/inbox', methods=['GET', 'POST'])
def inbox():
    print("loginId", session['loginId'])
    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))


    chats = ["Maria", "Joe", "Frank"]

    search_error=None

    if request.method == 'POST':

        # creating new chat
        if request.get_json()["type"] == 'new-chat':
            logins = req("get", "logins")
            loginId = 0
            for i in logins:
                if i['email'] == request.get_json()["email"]:
                    loginId = i['loginId']
            if loginId != 0:
                print("Found!:", loginId)

                data = {
                    'userId1' : session['loginId'],
                    'userId2' : loginId,
                }

                # check old chat to see if it exists
                old_chats = req('get', 'haschats')
                chat_found = False
                for chat in old_chats:
                    if (chat['userId1'] == data['userId1'] and chat['userId2'] == data['userId2']) or (chat['userId1'] == data['userId2'] and chat['userId2'] == data['userId1']):
                        chat_found = True

                # when old chat exists 
                if chat_found:
                    res = jsonify({"error": "already created"})
                    res.status_code = 304
                    print("chat already created")
                    return res
                else:
                    print("created")
                    created_chat = req('post', 'haschats', data=data)
                    res = jsonify({"error": "no error"})
                    res.status_code = 200
                    return res 
            else:
                res = jsonify({"error": 'email does not exist'})
                res.status_code = 500
                return res
                


    chats = []
    chats_reqs = req('get', 'haschats')
    for i in chats_reqs:
        if i['userId1'] == session['loginId']:
            other_user = req('get', 'logins', id=i['userId2'])
            chats.append([other_user['email'], i['hasChatId']])
        elif i['userId2'] == session['loginId']:
            other_user = req('get', 'logins', id=i['userId1'])
            chats.append([other_user['email'], i['hasChatId']])


    return render_template('inbox.html', chats=chats, messages=[], senders=[], len=0, search_error=search_error)

# Displays a user's chats and the messages in the selected chat
@app.route('/chat/<chat_id>', methods=['GET', 'POST'])
def chat(chat_id):
    
    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))


    # when message is sent from curent user
    if request.method == 'POST':
        print(request.get_json()["message"])

        message_data = {
            "chatId": chat_id,
            "timeStamp": 000,
            "userId": session['loginId'],
            "message": request.get_json()["message"]
        }

        send_message = req('post', 'messages', data=message_data)

        return redirect(url_for('chat', chat_id=chat_id))
    

    # get other persons email
    curr_chat = req("get", "haschats", id=chat_id)
    if curr_chat['userId1'] == session['loginId']:
        other = req('get', 'logins', id=curr_chat['userId2'])['email']
    elif curr_chat['userId2'] == session['loginId']:
        other = req('get', 'logins', id=curr_chat['userId1'])['email']

    # get messages
    messages = []
    message_reqs = req("get", "getmessagebychat", id=chat_id)
    for message in message_reqs:
        if message['userId'] == session['loginId']:
            messages.append([message['message'], 'user'])
        else:
            messages.append([message['message'], 'other'])

    # messages = [["message 1", "user"], ["message 2", "other"]]

    return render_template('chat.html', messages=messages, other=other)

# Displays all courses, along with a search bar + allows teachers to create a course
@app.route('/all-courses', methods=['GET', 'POST'])
def courses():

    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))
    
    courses = []
    request = req("get", "courses")
    for i in request:
        courses.append([i["name"], i["description"], i["courseId"]])

    if session["role"] == "teacher":
        isTeacher = True

    return render_template('all-courses.html', courses=courses, isTeacher = isTeacher)

# Displays a single course and its information
@app.route('/course/<courseId>', methods=['GET', 'POST'])
def course(courseId):

    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))

    modules = []
    assignments = []
    name = ""
    description=""

    # get course information
    request = req("get", "courses", id=courseId)
    name = request["name"]
    description = request["description"]

    # get modules
    request = req("get", "coursemodules", id=courseId)

    for i in request:
        module = req("get", "modules", id=i["moduleId"])
        modules.append([module["moduleId"], module["name"]])


    # get modules
    request = req("get", "assignmentsbycourse", id=courseId)

    for i in request:
        print(module)
        assignments.append([i["courseAssignmentId"], i["name"]])

    print("assignments", assignments)



    # This is temporary, for design purposes:
    return render_template('course.html', courseId=courseId, courseName=name, courseDesc=description, 
            courseModules=modules, courseAssignments=assignments)

# Displays a student's assignments
@app.route('/student-assignments', methods=['GET', 'POST'])
def studentAssignments():
    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))
    
    return render_template('student-assignments.html')

# Displays an assignment
@app.route('/assignments/<assignmentId>')
def assignment(assignmentId):

    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))

    request = req("get", "moduleAssignments", id=assignmentId)
    # courses.append([i["name"], i["description"], i["courseId"]])

    if session["role"] == "teacher":
        isTeacher = True
    
    return render_template('assignment.html', assignment = request)

# Displays the results of a search conducted from the 
@app.route('/results', methods=['GET', 'POST'])
def results():
    # need to get users and courses that match input in search bar
    users = []
    courses = []
    modules = []
    assignments = []

    return render_template('search-results.html', users=users, courses=courses, modules=modules, assignments=assignments)

# Displays the Module Documents of a Given Course  
@app.route('/course/<courseId>/moduleDocuments/<moduleId>', methods = ["GET", "POST"])
def moduleDocuments(courseId, moduleId):
    
    modules = []

    if session.get("loginId") is None:
        return redirect(url_for('log_in'))
        
    request = req('GET', "courses", id = courseId)

    for r in request:

        request_docs = req("GET", "moduleDocuments", id = moduleId)   
        modules.append(request_docs)


    return render_template('course.html', modules = modules)

# Displays the Module Assignments of a Given Course  
@app.route('/course/<courseId>/moduleDocuments/<moduleId>', methods = ["GET", "POST"])
def moduleAssignments(courseId, moduleId):
    
    modules = []

    if session.get("loginId") is None:
        return redirect(url_for('log_in'))
        
    request = req('GET', "courses", id = courseId)

    for r in request:

        request_docs = req("GET", "moduleAssignments", id = moduleId)   
        modules.append(request_docs)


    return render_template('course.html', modules = modules)

# Logs the user out
@app.route('/log-out', methods=['GET', 'POST'])
def logOut():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port="8000", debug=True)
