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

    fetch("/inbox", {
        method: "POST", 
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
                console.log("valid email");
            }
        })
    });
}


// get input from search and then reset input
document.querySelector('#search-bar').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        var input = document.getElementById('search-bar').value;
        document.getElementById("new-chat").style.display = 'block';
        document.getElementById("search-bar").style.display = 'none';
        sendToBackend(input)
    }
});

