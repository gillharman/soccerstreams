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
})

function onPageLoad(){
    //ADD WATCH GAME HANDLER ON MATCHES
    $(".match").click(function() {
            window.location = "watch_game/" + $(this).data("match-id")
    })
}



// $('#match-days-wrapper').remove();

//                $('#nav-title').text($(this).attr('data-league-name'));
//                $('#wrapper').removeClass('wrapper-outline');
//                $('#wrapper').append("<div class='loader' style='width: 30px; height: 30px; margin: 15px auto;'><div class='is-loading'></div></div>");
//                $.ajax({
//                    url: 'ajax/league_matches',
//                    async: true,
//                    data: {'league' : $(this).attr('data-league')},
//                    success: function(result) {
//                        $('.loader').remove();
//                        $('.is_loading').remove();
//                        $('#wrapper').append(result);
//                        $('#wrapper').addClass('wrapper-outline');
//                        onPageLoad();  // ADD HANDLERS AFTER THE AJAX CALL
//                    },
//                    error: function(result, exception) {
//                        var msg = '';
//                        if(result.responseText) {
//                            msg = result.responseText;
//                        } else {
//                            msg = 'Temporary Unavailable. Please try at a later time.'
//                        }
//                        $('.loader').remove();
//                        $('.is_loading').remove();
//                        $('#wrapper').html(msg);
//                        $('#wrapper').addClass('wrapper-outline');
//                    },
//                })