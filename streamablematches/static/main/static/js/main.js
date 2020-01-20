$(document).ready(function() {
    var selected_league = location.pathname.split('/')[1];
    if(selected_league != '' && selected_league != undefined) {
        $('#' + selected_league).addClass('active');
    } else {  // DEFAULT IS PL
        try {
            $('#PL').addClass('active');
        } catch(e) {}
    }
    var nav_pills = $('#nav-pills ul').children();
    if(nav_pills) {
        for (var i=0; i < nav_pills.length; ++i) {
            $(nav_pills[i]).on('click', function() {
                var league = $(this).attr('data-league');
                if(league == '' || league == undefined) {
                    window.location = '/';
                } else {
                    window.location = "/" + league;
                }
            })
        }
        onPageLoad();  // ADD HANDLERS AFTER THE FIRST TIME THE PAGE LOAD
    }

    var current_match_day = $("#current-match-day").val();
    if(current_match_day) {
      var position_from_top = $("#match-day-" + current_match_day).offset().top;
      position_from_top = position_from_top - 200;  // Scrolls the element into view.
      window.scroll(0, position_from_top);
    }
})

function onPageLoad(){
    // ADD CLICK HANDLER FOR USER PROFILE
    $(".dropdown").on("click", function() {
        if($("#user-profile-dropdown").hasClass("show")) {
            $("#user-profile-dropdown").removeClass("show");
        } else {
            $("#user-profile-dropdown").addClass("show");
        }
    })

    // ADD WATCH GAME HANDLER ON MATCHES
    $(".match").click(function() {
            window.location = "watch_game/" + $(this).data("match-id")
    })
}


// CLOSES THE DROPDOWN MENU IF THE USER CLICKS OUTSIDE OF IT
window.onclick = function(event) {
    if(!event.target.matches('.dropdown')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for(var i = 0; i < dropdowns.length; ++i) {
            var openDropdown = dropdowns[i];
            if(openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}