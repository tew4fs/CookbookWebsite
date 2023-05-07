let people_count = 0

function addPerson() {
    if (people_count < 50) {
        people_count++;
        var users = document.getElementById("users");
        var nextUser = document.createElement("input");
        nextUser.id = "person_"+people_count;
        nextUser.autocomplete = "off"
        nextUser.type = "email";
        nextUser.maxLength = 50;
        nextUser.placeholder = "Enter an Email";
        nextUser.className = "form-control";
        nextUser.required = "required";
        users.append(nextUser);
        return nextUser;
    }
}

function removePerson() {
    if(people_count > 0){
        var user = document.getElementById("person_"+people_count);
        user.remove();
        people_count--;
    }
}


function updatePeopleList(){
    var peopleList = document.getElementById("people-list");
    var list = document.getElementById("person_1").value;
    for(var person_num=2; person_num<=people_count; person_num++){
        var person = document.getElementById("person_" + person_num);
        list += "," + person.value;
    }
    peopleList.value = list;
    console.log(peopleList.value)
}