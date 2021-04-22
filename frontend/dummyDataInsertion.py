from req import req


# create student and teacher
teacher_data = {
    'email': 'teacher@gmail.com',
    'password': 'teacher@gmail.com',
}
teacher_login_req = req('post', 'logins', data=teacher_data)
print(teacher_login_req)
student_data = {
    'email': 'student@gmail.com',
    'password': 'student@gmail.com',
}
student_login_req = req('post', 'logins', data=student_data)
teacher_data = {
    'name': 'teacher',
    'email': 'teacher@gmail.com',
    'connected': 'true',
    'loginId': 1,
}
teacher_req = req('post', 'teachers', data=teacher_data)
student_data = {
    'name': 'student',
    'email': 'student@gmail.com',
    'connected': 'true',
    'loginId': 2,
}
student_req = req('post', 'students', data=student_data)

# create courses
data = {
    'name': 'OOP',
    'description': 'object oriented programming',
    'dueDate': 10241998,
}
course_req = req('post', 'courses', data=data)
data = {
    'name': 'SE',
    'description': 'Software Engineering',
    # 'dueDate': 10241998,
}
course_req = req('post', 'courses', data=data)

teacher_course_req  = req('post', 'teachercourses', data={'courseId':1, 'teacherId':1})
student_course_req  = req('post', 'studentcourses', data={'courseId':1, 'studentId':1})

# create modules and course-module relation
data = {
    'name': 'week 1',
    'description': 'week 1s module',
    'courseId': '1',
}
req_module = req('post', 'modules', data=data)

course_module_req = req('post', 'coursemodules', data={'courseId':1, 'moduleId':1})

# create assignments and course-assignments relation
data = {
    'courseId':1,
    'name':'hw1',
    'description': "week 1s hw",
    'dueDate':10241998
}
asignment_req = req('post', 'courseassignments', data=data)

