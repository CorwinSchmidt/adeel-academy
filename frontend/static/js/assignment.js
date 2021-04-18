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

function sendToBackendGrade(id, grade) {
    const data = {
        "type" : 'grade_submit',
        "studentAssignmentId" : id,
        "grade" : grade,
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

var buttons = document.getElementsByClassName('grade-sub');
var fields = document.getElementsByClassName('grade-form');
for (var i=0 ; i < buttons.length ; i++){
    (function(index){
    buttons[index].onclick = function(){
        // alert("I am button " + );
        // sendToBackend(fields[index].value);
        console.log(fields[index].value);
    };
    })(i)
}