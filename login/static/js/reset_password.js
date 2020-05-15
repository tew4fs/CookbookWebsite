function checkPasswordsMatch() {
    var password = $("#password_1").val();
    var confirmPassword = $("#password_2").val();
    if (password != confirmPassword)
        document.getElementById("password_2").style.border = "1px solid red";
    else
        document.getElementById("password_2").style.border = "1px solid green";
    if (confirmPassword == "") {
        document.getElementById("password_2").style.border = "0px solid green";
        document.getElementById("password_2").style.borderBottom = "2px solid rgba(0, 0, 0, .3)";
    }
}

function checkToSubmit() {
    var password = $("#password_1").val();
    var confirmPassword = $("#password_2").val();
    if (password != "" && password == confirmPassword)
        document.getElementById("button").disabled = false;
    else
        document.getElementById("button").disabled = true;
}


$(document).ready(function() {
    $("#password_1").keyup(checkPasswordsMatch);
    $("#password_2").keyup(checkPasswordsMatch);

    $("#password_1").keyup(checkToSubmit);
    $("#password_2").keyup(checkToSubmit);
});