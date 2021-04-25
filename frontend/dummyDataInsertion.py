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

course_list = []
# create courses
data = {
    'name': 'Object-Oriented Programming',
    'description': 'Class Variables, Class Objects, Inheritance, Polymorphism, Methods, Superclasses and Subclasses',
    'dueDate': 10242021,
}
data2 = {
    'name': 'Data Structures',
    'description': 'Arrays, Linked Lists, Dictionaries, Heaps, Priority Queues, Maps and Graphs',
    'dueDate': 10242021,
}
data3 = {
    'name': 'Principles of Machine Learning',
    'description': 'Supervised Learning, Unsupervised Learning and Reinforcement Learning',
    'dueDate': 10262021,
}
data4 = {
    'name': 'Introduction to Artificial Intelligence',
    'description': 'Graph Algorithms, A* Search, Hill Climbing, Simulated Annealing, KNN, Linear and Logistic Regression',
    'dueDate': 10282021,
}
data5 = {
    'name': 'Computer Vision',
    'description': 'K-Nearest Neighbors, Fast Fournier Transform, Convolutional Neural Networks, Recurrent Neural Network',
    'dueDate': 10292021,
}
data6 = {
    'name': 'Introduction to Statistical Inference',
    'description': 'P-Value and Normal Distributions, Generalized Linear Models and Bayesian Methods',
    'dueDate': 10312021,
}
data7 = {
    'name': 'Data Mining and Analysis',
    'description': 'Statistical Modeling, Data Cleansing, Classification, Regression and Clustering',
    'dueDate': 11032021,
}
data8 = {
    'name': 'Calculus II',
    'description': 'Integrals, Differential Equations, Parametric Equations, Polar Coordinates and Vector-Valued Functions',
    'dueDate': 11072021,
}
course_list.append(data)
course_list.append(data2)
course_list.append(data3)
course_list.append(data4)
course_list.append(data5)
course_list.append(data6)
course_list.append(data7)
course_list.append(data8)

course_req = req('post', 'courses', data=course_list)
data = {
    'name': 'SE',
    'description': 'Software Engineering',
    # 'dueDate': 10241998,
}
course_req = req('post', 'courses', data=course_list)



teacher_course_req  = req('post', 'teachercourses', data={'courseId':1, 'teacherId':1})
student_course_req  = req('post', 'studentcourses', data={'courseId':1, 'studentId':1})

# create modules and course-module relation
module_list = []

data = {
    'name': 'Module 1',
    'description': 'Week 1 Learning Module',
    'courseId': '1',
}
data2 = {
    'name': 'Module 2',
    'description': 'Week 2 Learning Module',
    'courseId': '1',
}
data3 = {
    'name': 'Module 3',
    'description': 'Week 3 Learning Module',
    'courseId': '1',
}
data4 = {
    'name': 'Module 4',
    'description': 'Week 4 Learning Module',
    'courseId': '1',
}
data5 = {
    'name': 'Module 5',
    'description': 'Week 5 Learning Module',
    'courseId': '1',
}
data6 = {
    'name': 'Module 6',
    'description': 'Week 6 Learning Module',
    'courseId': '1',
}
data7 = {
    'name': 'Module 7',
    'description': 'Week 7 Learning Module',
    'courseId': '1',
}
data8 = {
    'name': 'Module 8',
    'description': 'Week 8 Learning Module',
    'courseId': '1',
}

module_list.append(data)
module_list.append(data2)
module_list.append(data3)
module_list.append(data4)
module_list.append(data5)
module_list.append(data6)
module_list.append(data7)
module_list.append(data8)


req_module = req('post', 'modules', data=module_list)

course_module_req = req('post', 'coursemodules', data={'courseId':1, 'moduleId':1})

# create assignments and course-assignments relation
assignment_list = []


data = {
    'courseId':1,
    'name':'Assignment 1',
    'description': "Linearithmic Sorting Algorithms - Mergesort, Quicksort and Heapsort",
    'dueDate':10012021
}
data2 = {
    'courseId':1,
    'name':'Assignment 2',
    'description': "Search Algorithms on Linear Data Structures",
    'dueDate':10082021
}
data3 = {
    'courseId':1,
    'name':'Assignment 3',
    'description': "Depth First Search and Breadth First Search",
    'dueDate':10152021
}
data4 = {
    'courseId':1,
    'name':'Assignment 4',
    'description': "Graph Traversals - Preorder, Inorder and Postorder Tree Traversals",
    'dueDate':10222021
}
data5 = {
    'courseId':1,
    'name':'Assignment 5',
    'description': "Hashing and Key:Value Lookups - Mapping Keys to Values Efficiently",
    'dueDate':10292021
}
data6 = {
    'courseId':1,
    'name':'Assignment 6',
    'description': "Top-Down and Bottoms-up Programming - Solving Problems through Solving Subproblems",
    'dueDate':11052021
}
data7 = {
    'courseId':1,
    'name':'Assignment 7',
    'description': "String Matching and Parsing - KMP Algorithm and RegEx String Parsing",
    'dueDate':11122021
}
data8 = {
    'courseId':1,
    'name':'Assignment 8',
    'description': "Cryptography - RSA Algorithm",
    'dueDate':11192021
}

assignment_list.append(data)
assignment_list.append(data2)
assignment_list.append(data3)
assignment_list.append(data4)
assignment_list.append(data5)
assignment_list.append(data6)
assignment_list.append(data7)
assignment_list.append(data8)

assignment_req = req('post', 'courseassignments', data=assignment_list)

course_assignments_req = req('post', 'courseassignments', data = {'courseId' : 1})
