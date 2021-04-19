let url_base = "http://127.0.0.1:5000/";



document.getElementById("search").onclick = function () {
    var search_string = document.getElementById("search-bar").value;
    if (search_string != "") {
        
        var params_string = "";
    
        if (document.getElementById('courses').checked) {
            params_string += "%20courses";
        }
    
        if (document.getElementById('modules').checked) {
            params_string += "%20modules";
        }
    
        if (document.getElementById('assignments').checked) {
            params_string += "%20assignments";
        }

        var new_url = "";

        if (params_string == "") {
            new_url =
                "results/?search=" +
                search_string +
                "&&filter=all"
        } else {
            new_url = 
                "results/?search=" +
                search_string +
                "&&filter=" + params_string
        }
    
        console.log(params_string);
        console.log(search_string);
        console.log(new_url);

        window.location.replace(new_url)
    }
};