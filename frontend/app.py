import os
from re import sub
from typing import NamedTuple, NoReturn
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, Response
from flask_cors import CORS
from wtforms import Form, StringField, PasswordField, validators, SubmitField, RadioField
import requests
import json
from req import req
import smtplib
from email.message import EmailMessage

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
        print(courses)
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
    courses_req = req("get", "courses")
    for i in courses_req:
        courses.append([i["name"], i["description"], i["courseId"]])
    
    isTeacher = False
    if session["role"] == "teacher":
        isTeacher = True

    if request.method == 'POST':
        course_id = request.get_json()['courseId']
        
        if isTeacher:
            course_enroll_req = req(
                'post', 
                'teachercourses', 
                data = {
                    'courseId' : course_id,
                    'teacherId' : session['teacherId']
                }
            )
        else:
            course_enroll_req = req(
                'post', 
                'studentcourses', 
                data = {
                    'courseId' : course_id,
                    'studentId' : session['studentId']
                }
            )


        # print(request.get_json())
    return render_template('all-courses.html', courses=courses, isTeacher = isTeacher)

# Displays a single course and its information
@app.route('/course/<courseId>', methods=['GET', 'POST'])
def course(courseId):
    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))

    # when teacher set is_teacher to true in order to pass to template
    is_teacher = False
    if session.get("role") == 'teacher':
        is_teacher = True
        
            
    teacher_courses = req("GET", "teachercourses")
    student_courses = req("GET", "studentcourses")
    teachers = req("GET", "teachers")
    students = req("GET", "students")
    logins = req("GET", 'logins')
    module_recipients = []
    recipients = []

    # when post from frontend
    if request.method == 'POST':
        if request.get_json()['type'] == 'create_module':
            name = request.get_json()['name']
            description = request.get_json()['description']
            data={
                'name': name, 
                'description': description,
                'courseId': courseId,
            }
            posted_module = req("post", "modules", data=data)
            data = {
                'moduleId' : posted_module['moduleId'],
                'courseId' : courseId
            }
            posted_course_module = req("post", "coursemodules", data)
            
            if teacher_courses[courseId] == student_courses[courseId]:

                if teacher_courses['teacherId'] == teachers['teacherId']:

                    for student in student_courses:

                        id = student['studentId']

                        if students['studentId'] == id:

                            module_recipients.append(student['email'])
            msg = EmailMessage()
            msg['Subject'] = data['name']
            if teachers['loginId'] == logins['loginId']:

                msg['From'] = teachers['email']

            msg['To'] = module_recipients
            msg.set_content(data['desciption'])
    
            teacher_email = ''
            teacher_password = ''
            if teachers['loginId'] == logins['loginId']:

                teacher_email = logins['email']
                teacher_password = logins['password']

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:


                smtp.login(teacher_email, teacher_password)

                smtp.send_message(msg)
            
            print("posted", posted_module)
            return redirect('course', courseId)


        if request.get_json()['type'] == 'create_assignment':
            name = request.get_json()['name']
            description = request.get_json()['description']
            due_date = request.get_json()['dueDate'].replace("/","")
            print(request.get_json())
            data={
                'name': name, 
                'description': description,
                'dueDate': due_date,
                'courseId': courseId,
            }
            posted_assignment = req("post", "courseassignments", data=data)
            
            teacher_email2 = ''
            teacher_password2 = ''

            if teacher_courses[courseId] == student_courses[courseId]:

                if teacher_courses['teacherId'] == teachers['teacherId']:

                    for student in student_courses:
                        
                        id = student['studentId']

                        if students['studentId'] == id:

                            recipients.append(student['email'])

            a_msg = EmailMessage()
            a_msg['Subject'] = data['name']

            if teachers['loginId'] == logins['loginId']:

                a_msg['From'] = teachers['email']
            
            a_msg['To'] = recipients
            a_msg.set_content(data['description'])

            if teachers['loginId'] == logins['loginId']:

                teacher_email2 = logins['email']
                teacher_password2 = logins['password']

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

                smtp.login(teacher_email2, teacher_password2)

                smtp.send_message(a_msg)

            print(posted_assignment)
            return redirect(url_for('course', courseId=courseId))

        
        if request.get_json()['type'] == 'create_announcement':

            name = request.get_json()['name']
            description = request.get_json()['description']
            timestamp = request.get_json()['timeStamp'].replace("/","")
            print(request.get_json())

            data = {
                'name' : name,
                'description' : description,
                'timeStamp' : timestamp, 
                'courseId' : courseId
            }
            posted_announcement = req('POST', 'announcements', data = data)

            t_email = ''
            t_password = ''

            if teacher_courses[courseId] == student_courses[courseId]:

                if teacher_courses['teacherId'] == teachers['teacherId']:

                    for student in student_courses:
                        
                        id = student['studentId']

                        if students['studentId'] == id:

                            announcement_recipients.append(student['email'])

            announcement_msg = EmailMessage()
            announcement_msg['Subject'] = data['name']

            if teachers['loginId'] == logins['loginId']:

                announcement_msg['From'] = teachers['email']

            announcement_msg['To'] = announcement_recipients
            announcement_msg.set_content(data['description'])

            if teachers['loginId'] == logins['loginId']:

                t_email = logins['email']
                t_password = logins['password']

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

                smtp.login(t_email, t_password)

                smtp.send_message(announcement_msg)

            print(posted_announcement)
            return redirect(url_for('course', courseId = courseId))  

    modules = []
    assignments = []
    name = ""
    description=""

    # get course information
    course = req("get", "courses", id=courseId)
    name = course["name"]
    description = course["description"]

    # get modules
    req_modules = req("get", "coursemodules", id=courseId)

    for i in req_modules:
        module = req("get", "modules", id=i["moduleId"])
        modules.append([module["moduleId"], module["name"]])


    # get assignments
    assignment_reqs = req("get", "assignmentsbycourse", id=courseId)
    assignments = []
    for i in assignment_reqs:
        assignments.append([i["courseAssignmentId"], i["name"]])



    #get announcements
    #req_announcements = req('get', 'announcements', id = courseId)

    #for i in req_announcements:

        #annoucement = req('get', 'announcements', id = i['announcementId'])
        #announcements.append([annoucement['announcementId'], annoucement['name']])

    # This is temporary, for design purposes:
    return render_template(
        'course.html', 
        courseId=courseId, 
        courseName=name, 
        courseDesc=description, 
        courseModules=modules, courseAssignments=assignments,
        is_teacher = is_teacher)

# Displays a student's assignments
@app.route('/student-assignments', methods=['GET', 'POST'])
def studentAssignments():
    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))
    
    return render_template('student-assignments.html')

# Displays an assignment
@app.route('/assignments/<assignmentId>', methods=['GET', 'POST'])
def assignment(assignmentId):

    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))

    assignment_req = req("get", "courseassignments", id=assignmentId)
    date = str(assignment_req['dueDate'])
    assignment_req['dueDate'] = date[:2] + '/' + date[2:4] + "/" + date[4:]


    course_req = req("get", "courses", id=assignment_req['courseId'])
    submitted = ''
    text = ''
    submissions = []
    is_teacher = False
    if session["role"] == "teacher":
        is_teacher = True
        # get all student submissions for current courses
        submissions_req = req('get', 'studentassignments')
        submissions = []
        for i in submissions_req:
            if i['courseAssignmentId'] == int(assignmentId):
                print("found")
                student_req = req('get', 'students', id=i['studentId'])
                submissions.append({
                    "name": student_req['name'],
                    "grade": i['grade'],
                    "text": i['text'],
                    "studentAssignmentId": i['studentAssignmentId']
                })
        print(submissions)

    if not is_teacher:
        # find if assignment is already complete by current student
        student_assignment_req = req('get', 'studentassignments')
        submitted = False
        text = ''
        for i in student_assignment_req:
            if int(i['courseAssignmentId']) == int(assignmentId) and int(i['studentId']) == int(session['studentId']):
                submitted = True
                text = i['text']
                break
            
    if request.method == 'POST' and request.get_json()['type'] == 'student_submit':
        # insert students submission into api
        data = {
            'courseAssignmentId': assignmentId,
            'studentId': session['studentId'],
            'text': request.get_json()['text'],
            'grade': -1
        }
        text_req = req('post', 'studentassignments', data=data)
        print(text_req)

    
    return render_template('assignment.html', 
        assignment = assignment_req, 
        course = course_req,
        is_teacher= is_teacher,
        submitted=submitted,
        text=text,
        submissions=submissions)

@app.route('/results/', methods=['GET', 'POST'])
def results():

    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))

    # http://127.0.0.1:8000/results/?search=asdf
    courses = []
    modules = []
    assignments = []

    '''
    # courses request carries:
        course:
            id
            name
            description
        assignments:
            id
            name
            description
        modules:
            id
            name
            description
    '''   

    course_req = req('get', 'courses')

    # course object contains course data, assignment data, and module data
    for course in course_req:
        course_dic = {
            'type': 'course',
            'id': course['courseId'],
            'name': course['name'],
            'description': course['description'],
        }
        courses.append(course_dic)

        for assignment in course['assignments']:
            assignment_dic = {
                'type': 'assignment',
                'id': assignment['courseAssignmentId'],
                'name': assignment['name'],
                'description': assignment['description'],
            }
            assignments.append(assignment_dic)

        for module in course['modules']:
            module_dic = {
                'type': 'module',
                'id': module['moduleId'],
                'name': module['name'],
                'description': module['description'],
            }
            modules.append(module_dic)
    
    search_string = request.args.get('search').replace("%20", " ")
    search_params = request.args.get('filter').replace("%20", " ")
    params_list = search_params.split()

    results = []

    def query_courses():
        for course in courses:
            # if search matches name or description of course
            if search_string in course.get('name') or search_string in course.get('description'):
                results.append(course)
    def query_modules():
        for module in modules:
            # if search matches name or description of course
            if search_string in module.get('name') or search_string in module.get('description'):
                results.append(module)
    def query_assignments():
        for assignment in assignments:
            # if search matches name or description of course
            if search_string in assignment.get('name') or search_string in assignment.get('description'):
                results.append(assignment)

    if params_list[0] == 'all':
        query_courses()
        query_modules()
        query_assignments()
    
    if 'modules' in params_list:
        query_modules()
        
    if 'assignments' in params_list:
        query_assignments()

    if 'courses' in params_list:
        query_courses()

    print("results")
    print(results)

    return render_template('search-results.html', results=results)

@app.route('/search')
def search():

    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))

    return render_template('search.html')


# module page
@app.route('/module/<module_id>')
def modules(module_id):

    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))

    module_req = req('get', 'modules', id=module_id)

    is_teacher = False
    if session['role'] == 'teacher': is_teacher = True


    return render_template('module.html', module=module_req, is_teacher=is_teacher)


# Displays the Module Documents of a Given Course  
@app.route('/course/<courseId>/moduleDocuments/<moduleId>', methods = ["GET", "POST"])
def moduleDocuments(courseId, moduleId):

    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))
    
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

    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))
    
    modules = []

    if session.get("loginId") is None:
        return redirect(url_for('log_in'))
        
    request = req('GET', "courses", id = courseId)

    for r in request:

        request_docs = req("GET", "moduleAssignments", id = moduleId)   
        modules.append(request_docs)


    return render_template('course.html', modules = modules)

@app.route('/announcement/<annoucementId>', methods = ["GET", "POST"])
def announcement(announcementId):

    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))

    # query announcements
    request = req('GET', "announcements", id = announcementId)

    return render_template('announcement.html', announcement = request)

@app.route('/user/<loginId>', methods=['GET', 'POST'])
def user(loginId):

    #  when not logged in, redirect to login page
    if session.get("loginId") is None:
        return redirect(url_for('log_in'))

    # TODO: Query logins

    # return redirect(url_for('user'), user = request, userType = userType)

    courses = [{'name':'Course 1'}, {'name':'Course 2'}]

    # temporary return
    return render_template('user.html', name = 'Example user', userType = 'Teacher', email = 'example@gmail.com',
        courses = courses, numCourses = len(courses))

# Logs the user out
@app.route('/log-out', methods=['GET', 'POST'])
def logOut():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port="8000", debug=True)
