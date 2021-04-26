from req import req

# create student and teacher
teacher_data = {
    'email': 'teacher@gmail.com',
    'password': 'teacher@gmail.com',
}
teacher_login_req = req('post', 'logins', data=teacher_data)

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

course_id = 1

for i in course_list:
    course_req = req('post', 'courses', data=i)


for i in range(1, len(course_list) - 2):
    teacher_course_req  = req('post', 'teachercourses', data={'courseId':i, 'teacherId':1})
    student_course_req  = req('post', 'studentcourses', data={'courseId':i, 'studentId':1})

# create modules and course-module relation
for i in range(1, 7):
    for j in range(1, 9):
        data = {
            'name': 'Module ' + str(i),
            'description': 'Week' + str(i)+ 's Learning Module',
            'courseId': j,
        }

        req_module = req('post', 'modules', data=data)

        req_module_course = req('post', 'coursemodules', data={
            'courseId': j,
            'moduleId': req_module['moduleId']
        })

        assignment_data = {
            'courseId':j,
            'name':'Assignment ' + str(i),
            'description': "This is an assignment, it is called: Assignment" + str(i) ,
            'dueDate':10012021
        }

        req_assignment = req('post', 'courseassignments', data=assignment_data)


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