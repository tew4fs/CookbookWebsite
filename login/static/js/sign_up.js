function checkEmailsMatch(){
    var email = $("#email_1").val();
    var confirmEmail = $("#email_2").val();
    if (email != confirmEmail)
        document.getElementById("email_2").style.border="1px solid red";
    else
        document.getElementById("email_2").style.border="1px solid green";
    if (confirmEmail == ""){
        document.getElementById("email_2").style.border="0px solid green";
        document.getElementById("email_2").style.borderBottom="2px solid rgba(0, 0, 0, .3)";
    }
}

$(document).ready(function () {
    $("#email_1").keyup(checkEmailsMatch);
    $("#email_2").keyup(checkEmailsMatch);
 });

 function checkPasswordsMatch(){
    var password = $("#password_1").val();
    var confirmPassword = $("#password_2").val();
    if (password != confirmPassword)
        document.getElementById("password_2").style.border="1px solid red";
    else
        document.getElementById("password_2").style.border="1px solid green";
    if (confirmPassword == ""){
        document.getElementById("password_2").style.border="0px solid green";
        document.getElementById("password_2").style.borderBottom="2px solid rgba(0, 0, 0, .3)";
    }
}

$(document).ready(function () {
    $("#password_1").keyup(checkPasswordsMatch);
    $("#password_2").keyup(checkPasswordsMatch);
 });

