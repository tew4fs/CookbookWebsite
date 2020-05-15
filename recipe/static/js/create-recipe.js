function onLoad() {
    var i = 1;
    while (i < 4) {
        var steps = document.getElementById("steps");
        var nextStep = document.createElement("textarea");
        nextStep.name = i;
        nextStep.maxLength = 300;
        nextStep.placeholder = "Step " + i;
        nextStep.required = "required";
        nextStep.className = "form-control";
        steps.append(nextStep);

        i++
    }
    i = 101;
    while (i < 104) {
        var ingredients = document.getElementById("ingredients");
        var nextStep = document.createElement("textarea");
        nextStep.name = i;
        nextStep.maxLength = 100;
        nextStep.placeholder = "Ingredient " + (i - 100);
        nextStep.required = "required";
        nextStep.className = "form-control";
        ingredients.append(nextStep);
        i++;
    }
    document.getElementById("food-pic").style.display = "none";
}


function addStep() {
    var steps = document.getElementById("steps");
    var lastStep = steps.lastElementChild;
    var nextStep = document.createElement("textarea");
    var num = parseInt(lastStep.name) + 1;
    if (num < 51) {
        nextStep.name = num;
        nextStep.maxLength = 300;
        nextStep.placeholder = "Step " + num;
        nextStep.required = "required";
        nextStep.className = "form-control";
        steps.append(nextStep);
    }
}

function removeStep() {
    var steps = document.getElementById("steps");
    var lastStep = steps.lastElementChild;
    var num = parseInt(lastStep.name);
    if (num > 1) {
        lastStep.remove();
    }
}


function addIngredient() {
    var ingredients = document.getElementById("ingredients");
    var lastStep = ingredients.lastElementChild;
    var nextStep = document.createElement("textarea");
    var num = parseInt(lastStep.name) + 1;
    if (num < 151) {
        nextStep.name = num;
        nextStep.maxLength = 100;
        nextStep.placeholder = "Ingredient " + (num - 100);
        nextStep.required = "required";
        nextStep.className = "form-control";
        ingredients.append(nextStep);
    }
}

function removeIngredient() {
    var ingredients = document.getElementById("ingredients");
    var lastStep = ingredients.lastElementChild;
    var num = parseInt(lastStep.name);
    if (num > 101) {
        lastStep.remove();
    }
}

function readURL(input) {
    if (input.files && input.files[0]) {
        var str = input.files[0].name;
        var fileType = str.substr(str.length - 4);
        if (fileType != "jpeg" && fileType != ".jpg" && fileType != ".png" && fileType != '.JPG' && fileType != '.PNG') {
            document.getElementById("file-up").value = "";
            document.getElementById("food-pic").style.display = "none";
        } else {
            document.getElementById("food-pic").style.display = "inline";
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#food-pic')
                    .attr('src', e.target.result)
                    .width(200)
                    .height(200);
            };
            reader.readAsDataURL(input.files[0]);
        }
    }
}

$(document).ready(function() {
    onLoad();
});