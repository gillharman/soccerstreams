$(function() {
    var currentImage = $(".preview img").get(0) ? $(".preview img").attr("src") : null
    localStorage.userAvatar = currentImage;

    $("#id_avatar").on("change", updateImageDisplay);
    $(".selected-file .btn").on("click", removeFile);
});

function updateImageDisplay() {
    var preview = $(".preview").get(0);
    var input = $("#id_avatar").get(0);

    var curFiles = input.files;
    if(curFiles.length > 0) {
        $("#form-errors").hide();  // Hide any previously placed error messages
        for(var i = 0; i < curFiles.length; i++) {
            $(".selected-file .file-name").text(curFiles[i].name);
            $(".selected-file").css("display", "flex");
            if(validFileType(curFiles[i])) {
                while(preview.firstChild) {
                    preview.removeChild(preview.firstChild);
                }
                var image = document.createElement('img');
                image.src = window.URL.createObjectURL(curFiles[i]);
                image.width = 70;
                image.height = 70;

                preview.appendChild(image);
            } else {
                var errorCol = $("#form-errors .col");
                errorCol.text("Invalid image format. Supported image formats are jpeg, pjpeg or png.");
                $("#form-errors").show();
            }
        }
    }
}

function removeFile() {
    var input = $("#id_avatar").get(0);
    var preview = $(".preview").get(0);

    var curFiles = input.files;
    if(validFileType(curFiles[0])) {
        while(preview.firstChild) {
            preview.removeChild(preview.firstChild);
        }
        if(localStorage.userAvatar == "null") {
            $(".preview").html("<i class='fa fa-user-circle'></i>")
        } else {
            var image = document.createElement('img');
            image.src = localStorage.userAvatar;
            image.width = 70;
            image.height = 70;

            preview.appendChild(image);
        }
    }

    $("#id_avatar").val("");
    $(".selected-file .file-name").text("");
    $(".selected-file").hide();
}

var fileTypes = [
    'image/jpeg',
    'image/pjpeg',
    'image/png'
]

function validFileType(file) {
    for(var i = 0; i < fileTypes.length; i++) {
        if(file.type === fileTypes[i]) {
            return true;
        }
    }

    return false;
}