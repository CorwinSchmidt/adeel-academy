let url_base = "http://127.0.0.1:5000/" 



function sendToBackend(userId, role) {
    const data = {
        "userId": userId,
        "role": role,
    };

    console.log(data);

    // send user info to flask to create session
    console.log(json)
    fetch('/log-in', {
        method: "POST", 
        body : JSON.stringify(data), 
        headers: {
            'Content-Type': 'application/json', 
            'Accept': 'application/json',
            "Access-Control-Allow-Origin": "*",}
    // redirect to dashboad on success
    }).then(window.location.replace(window.location.origin + "/dashboard"));
}


// initiates the sign in process
function logIn(method, url) {

    // get data from form
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;


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
                console.log("trying to show error");
                // show error for creation
                console.log(response.status);
                document.getElementById("error").style.display = 'block';
                document.getElementById("error").innerHTML ="<p>Error loggin into your account, please try again.</p>";
            } else {
                sendToBackend(json["userId"], json["role"]);
            }
        })
    });
}
