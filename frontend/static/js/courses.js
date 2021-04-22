let url_base = "http://127.0.0.1:5000/" 

function newCourse() {
    // display screen to enter course details
}

function createCourse() {
    // based on entered details, create the new course
}

function sendToBackend(id) {
    const data = {
        "courseId" : id,
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
                console.log("error sending course to backend");
            }
        });
    });
}

var buttons = document.getElementsByClassName('register');
for (var i=0 ; i < buttons.length ; i++){
    (function(index){
    buttons[index].onclick = function(){
        sendToBackend(buttons[index].id);
    };
    })(i)
}