document.getElementById("assignment").onclick = function () { 
    document.getElementById("assignment-text").style.display='block';
    document.getElementById("submit-assignment").style.display='block';
    document.getElementById("assignment").style.display='none';
};

document.getElementById("submit-assignment").onclick = function () {
    var text = document.getElementById("assignment-text").value;
    document.getElementById("assignment-text").style.display='none';
    document.getElementById("submit-assignment").style.display='none';
    document.getElementById("assignment").style.display='block';
    if (text !== '') {
        sendToBackend(text);
    } else {
        console.log("empty arguments");
    }

};

function sendToBackend(text) {
    const data = {
        "type" : "student_submit",
        "text": text,
    };

    console.log(data);
    fetch(window.location.href, {
        method: "POST", 
        body : JSON.stringify(data), 
        headers: {
            'Content-Type': 'application/json', 
            'Accept': 'application/json'}
    }).then(response => {
        response.json().then(json => {
            // code that can access both here
            if (response.status >= 400){
                console.log("error sending assignment to backend");
            }
        });
    });
}