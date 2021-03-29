let url_base = "http://127.0.0.1:5000/" 


// this function creates a user or teacher based on the signup input
function createTeacherOrStudent(method, loginId, email, name) {


    var url_ext = "";

    // set where to post to 
    if(document.getElementById("teacher").checked) {
        // teacher
        url_ext = 'teachers';
    } else {
        url_ext = 'students';

    }

    
    // data to send to backend 
    const data =  {
        'name': name,
        'email': email,
        'connected': "true",
        'loginId': loginId,

    }

    // create student/teacher
    fetch(url_base + url_ext, {
        method: method, 
        body : JSON.stringify(data), 
        headers: {
            'Content-Type': 'application/json', 
            'Accept': 'application/json'}
    }).then(response => {
        response.json().then(json => {
            if (response.status >= 400){
                console.log(response.status);
            } else {
                console.log(json)
                // update flask session so it knows userId and role(teacher/student)
                fetch('/sign-up', {
                    method: "POST", 
                    body : JSON.stringify(
                        {"userId":json["userId"],
                            "role": url_ext
                        }), 
                    headers: {
                        'Content-Type': 'application/json', 
                        'Accept': 'application/json'}
                }).then(
                    // if session created, send user to dashboard
                    window.location.replace(window.location.origin + "/dashboard")
                );
            }
        })
    });
}

// initiates the sign in process
function signUp(method, url) {

    // get data from form
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var name = document.getElementById("name").value;


    const data =  {
        'email': email,
        'password': password,
    }

    fetch(url_base + url, {
        method: method, 
        body : JSON.stringify(data), 
        headers: {
            'Content-Type': 'application/json', 
            'Accept': 'application/json'}
    }).then(response => {
        response.json().then(json => {
            // code that can access both here
            if (response.status >= 400){
                // show error for creation
                console.log(response.status);
                document.getElementById("error").style.display = 'block';
                document.getElementById("error").innerHTML ="<p>Error creating your account, please try again.</p>";
            } else {

                // create student or teacher based on insertion
                console.log(json)
                createTeacherOrStudent('POST', json['loginId'], email, name)
            }
        })
    });
}
