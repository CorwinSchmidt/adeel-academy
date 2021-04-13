// send message
document.querySelector('#chat-bar').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        var input = document.getElementById('chat-bar').value;
        document.getElementById('chat-bar').value = '';

        sendToBackend(input)
    }
});


function sendToBackend(message) {
    const data = {
        "message": message,
    };

    console.log(data);
    fetch(window.location.href, {
        method: "POST", 
        body : JSON.stringify(data), 
        headers: {
            'Content-Type': 'application/json', 
            'Accept': 'application/json'}
    }).then(function() {
        location.reload(); 
        console.log("reload");
    });
}
