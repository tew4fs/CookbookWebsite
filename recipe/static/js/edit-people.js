function addPerson() {
    var users = document.getElementById("users");
    var lastUser = users.lastElementChild;
    var nextUser = document.createElement("input");
    var num = parseInt(lastUser.name) + 1;
    if (num < 51) {
        nextUser.name = num;
        nextUser.autocomplete = "off"
        nextUser.type = "email";
        nextUser.maxLength = 50;
        nextUser.placeholder = "Enter an Email";
        nextUser.className = "form-control";
        users.append(nextUser);
    }
}

function removePerson() {
    var users = document.getElementById("users");
    var lastUser = users.lastElementChild;
    var num = parseInt(lastUser.name);
    if (num > 0) {
        lastUser.remove();
    }
}