function signup(user_id, group_id, lab_name, signed_up_students, max_students) {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    var http = new XMLHttpRequest();
    http.open("POST", '');
    http.setRequestHeader("X-CSRFToken", csrftoken); 
    var data = new Object();
    data.user_id = user_id;
    data.group_id = group_id;

    http.onreadystatechange = function () {
      if (http.readyState === 4){
        if (http.status === 200 && signed_up_students < max_students) {
          update_signed_up_students(group_id, max_students);
          alert("ilmoittautuminen työhön " + lab_name + " onnistui");
        }
        else {
          alert("ilmoittautuminen työhön " + lab_name + " epäonnistui");
        }
      }
    }
    http.send(JSON.stringify(data));
  }

function update_signed_up_students(group_id, max_students) {
    students = parseInt(document.getElementById("signed_up" + group_id).innerHTML);
    if (students < max_students){
      document.getElementById("signed_up" + group_id).innerHTML = students + 1;
    } else {
      alert("Ryhmä on jo täynnä");
    }
  }
  