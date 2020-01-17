$(document).ready(function() {
    $("#aboutMe").on("click", openAboutMeModal);
    $(".close-button .fa.fa-times").on("click", closeAboutMeModal);
});

function openAboutMeModal() {
    $("#aboutMeModal").show();
}

function closeAboutMeModal() {
    $("#aboutMeModal").hide();
}

var aboutMeModal = document.getElementById("aboutMeModal");
window.onclick = function(event) {
    if(event.target == aboutMeModal) {
        closeAboutMeModal();
    }
}