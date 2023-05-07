let ingredientCount = 0
let stepCount = 0

function addStep() {
    if (stepCount < 100){
        stepCount++;
        var steps = document.getElementById("steps");
        var nextStep = document.createElement("textarea");
        nextStep.id = "step_" + stepCount;
        nextStep.maxLength = 300;
        nextStep.placeholder = "Step " + stepCount;
        nextStep.required = "required";
        nextStep.className = "form-control";
        steps.append(nextStep);
        return nextStep
    }
}

function removeStep() {
    if (stepCount > 1){
        var steps = document.getElementById("steps");
        var lastStep = steps.lastElementChild;
        lastStep.remove();
        stepCount--;
    }
}

function updateStepList(){
    var stepsList = document.getElementById("steps-list");
    var list = document.getElementById("step_1").value;
    for(var step_num=2; step_num<=stepCount; step_num++){
        var step = document.getElementById("step_" + step_num);
        list += ", " + step.value;
    }
    stepsList.value = list;
}

function addIngredient() {
    if (ingredientCount < 100){
        ingredientCount++;
        var ingredients = document.getElementById("ingredients");
        var nextIngredient = document.createElement("textarea");
        nextIngredient.id = "ingredient_" + ingredientCount;
        nextIngredient.maxLength = 100;
        nextIngredient.placeholder = "Ingredient " + ingredientCount;
        nextIngredient.required = "required";
        nextIngredient.className = "form-control";
        ingredients.append(nextIngredient);
        return nextIngredient
    }
}

function removeIngredient() {
    if (ingredientCount > 1){
        var ingredients = document.getElementById("ingredients");
        var lastIngredient = ingredients.lastElementChild;
        lastIngredient.remove();
        ingredientCount--;
    }
}

function updateIngredientList(){
    var ingredientsList = document.getElementById("ingredients-list");
    var list = document.getElementById("ingredient_1").value;
    for(var ingredient_num=2; ingredient_num<=ingredientCount; ingredient_num++){
        var ingredient = document.getElementById("ingredient_" + ingredient_num);
        list += ", " + ingredient.value;
    }
    ingredientsList.value = list;
}

function updateLists(){
    updateIngredientList();
    updateStepList();
}

function onLoad() {
    addIngredient()
    addIngredient()
    addIngredient()
    addStep()
    addStep()
    addStep()
    document.getElementById("food-pic").style.display = "none";
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