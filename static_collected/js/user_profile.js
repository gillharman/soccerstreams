$(function() {
    $("#id_avatar").on("change", updateImageDisplay);
});

function updateImageDisplay() {
    var preview = $(".preview").get(0);
    var input = $("#id_avatar").get(0);

    var curFiles = input.files;
    if(curFiles.length > 0) {
        $("#form-errors").hide();  // Hide any previously placed error messages
        for(var i = 0; i < curFiles.length; i++) {
            $(".file-selector-label").text(curFiles[i].name);
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