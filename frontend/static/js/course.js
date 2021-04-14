document.getElementById("create-module").onclick = function () { 
    document.getElementById("module-name").style.display='block';
    document.getElementById("module-description").style.display='block';
    document.getElementById("send-module").style.display='block';
    document.getElementById("create-module").style.display='none';
};

document.getElementById("send-module").onclick = function () { 
    document.getElementById("module-name").style.display='none';
    document.getElementById("module-description").style.display='none';
    document.getElementById("send-module").style.display='none';
    document.getElementById("create-module").style.display='block';
    var name = document.getElementById("module-name").value;
    var description = document.getElementById("module-description").value;
    if (name !== '' && description !== '' ) {
        sendToBackendModule(name, description);
    }

};


function sendToBackendModule(name, description) {
    const data = {
        "type" : "create_module",
        "name" : name, 
        "description": description,
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
                console.log("error sending module to backend");
            }
        });
    });
}

document.getElementById("create-assignment").onclick = function () { 
    document.getElementById("assignment-name").style.display='block';
    document.getElementById("assignment-description").style.display='block';
    document.getElementById("send-assignment").style.display='block';
    document.getElementById("assignment-duedate").style.display='block';
    document.getElementById("create-assignment").style.display='none';
};

function sendToBackendAssignment(name, description, due_date) {
    const data = {
        "type" : "create_assignment",
        "name" : name, 
        "description": description,
        "dueDate": due_date,
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
                console.log("error sending module to backend");
            }
        });
    });
}

document.getElementById("send-assignment").onclick = function () {
    console.log("sending assignment") 
    document.getElementById("assignment-name").style.display='none';
    document.getElementById("assignment-description").style.display='none';
    document.getElementById("send-assignment").style.display='none';
    document.getElementById("assignment-duedate").style.display='none';
    document.getElementById("create-assignment").style.display='block';
    var name = document.getElementById("assignment-name").value;
    var description = document.getElementById("assignment-description").value;
    var due_date = document.getElementById("assignment-duedate").value;
    if (name !== '' || description !== ''|| due_date !== '') {
        if(isValidDate(due_date)) {
            sendToBackendAssignment(name, description, due_date);
            console.log("date validated");
        } else {
            console.log("error with data validaiton");
        }
    } else {
        console.log("empty arguments");
    }

};

// https://stackoverflow.com/questions/6177975/how-to-validate-date-with-format-mm-dd-yyyy-in-javascript
function isValidDate(dateString) {
    // First check for the pattern
    if(!/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(dateString))
        return false;

    // Parse the date parts to integers
    var parts = dateString.split("/");
    var day = parseInt(parts[1], 10);
    var month = parseInt(parts[0], 10);
    var year = parseInt(parts[2], 10);

    // Check the ranges of month and year
    if(year < 1000 || year > 3000 || month == 0 || month > 12)
        return false;

    var monthLength = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ];

    // Adjust for leap years
    if(year % 400 == 0 || (year % 100 != 0 && year % 4 == 0))
        monthLength[1] = 29;

    // Check the range of the day
    return day > 0 && day <= monthLength[month - 1];
};