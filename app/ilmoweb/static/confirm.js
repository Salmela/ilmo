function confirm(group_id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    var http = new XMLHttpRequest();
    http.open("POST", 'confirm/');
    http.setRequestHeader("X-CSRFToken", csrftoken); 
    var data = new Object();
    data = group_id
    http.send(JSON.stringify(data));

    document.getElementById("confirm" + group_id).innerHTML = "Vahvistettu"
}
