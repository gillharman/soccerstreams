$(document).ready(function() {
    //ADD OUTLINED BORDER TO AUTO-FOCUSED ELEMENTS
    var divId = $("input[autofocus]")[0].id.replace("id_", "");
    $("#" + divId + " .auth-form-field-border").addClass("auth-form-field-border-outline");

    //ADD "input-dirty" TO PRE-FILLED FIELDS
    var inputFields = $(".auth-field-container input");
    for(var inputField = 0; inputField < inputFields.length; ++inputField) {
        var inputID = inputFields[inputField].id;
        var divSelector = "#" + inputID.replace("id_", "");
        if($("#" + inputID).val() != "" && $("#" + inputID).val() != undefined) {
            $(divSelector).addClass("input-dirty");
        }
    }

    $(".auth-field-container input").on("focus", function(e) {
        var divId = "#" + $(e.target)[0].id.replace("id_", "");
        $(divId + " .auth-form-field-border").addClass("auth-form-field-border-outline");
    });

    $(".auth-field-container input").on("blur", function(e) {
       var divId = "#" + $(e.target)[0].id.replace("id_", "");
       $(divId + " .auth-form-field-border").removeClass("auth-form-field-border-outline");
    });

    $(".auth-field-container input").on("keyup", function(e) {
        var divId = "#" + $(e.target)[0].id.replace("id_", "");
        if($(e.target).val() != "" && $(e.target).val() != undefined) {
            $(divId).addClass("input-dirty");
        }
        else {
            $(divId).removeClass("input-dirty");
        }
    });
})