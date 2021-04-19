// This script is for searching for a user

let url_base = "http://127.0.0.1:5000/" 


function newChatSearch() {
    document.getElementById("new-chat").style.display = 'none';
    document.getElementById("search-bar").style.display = 'block';

}

function sendToBackend(email) {
    const data = {
        "type": "new-chat",
        "email": email,
    };

    console.log(data);
    var found  = false;
    fetch("/inbox", {
        method: "POST", 
        body : JSON.stringify(data), 
        headers: {
            'Content-Type': 'application/json', 
            'Accept': 'application/json'}
    }).then(response => {
        response.json().then(json => {
            // code that can access both here
            if (response.status == 500){
                console.log("trying to show error");
                // show error for creation
                // console.log(response.status);
                document.getElementById('err').innerHTML  = "<p style='color:red'>Email does not exist</p>";
            } else if (response.status == 304) {
                console.log("chat already created")
                document.getElementById('err').innerHTML  = "<p style='color:yellow'>Chat already created</p>";
            } else {
                console.log("valid email");
                document.getElementById('err').innerHTML  = "<p style='color:green'>Chat created!</p>";
            }
        })
    });


}


function displayError() {
    document.getElementById('err').innerHTML  = "<p>Error</p>"
}

// get input from search and then reset input
document.querySelector('#search-bar').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        var input = document.getElementById('search-bar').value;
        document.getElementById("search-bar").value= '';
        sendToBackend(input)
    }
});



