$(document).ready(function() {
    var nav_pills = $('#nav-pills ul').children();
    for (var i=0; i < nav_pills.length; ++i) {
        $(nav_pills[i]).on('click', function() {
            $('.nav-pill.active').removeClass('active');
            $(this).addClass('active');
            $('#nav-title').text($(this).attr('data-league-name'));
            $('#match-days').remove();
            $('#wrapper').append("<div class='loader' style='width: 30px; height: 30px; margin: 15px auto;'><div class='is-loading'></div></div>");
            $.ajax({
                url: 'ajax/league_matches',
                async: true,
                data: {'league' : $(this).attr('data-league')},
                success: function(result) {
                    $('.loader').remove();
                    $('.is_loading').remove();
                    $('#wrapper').append(result);
                },
                error: function(result, exception) {
                    var msg = '';
                    if(result.responseText) {
                        msg = result.responseText;
                    } else {
                        msg = 'Temporary Unavailable. Please try at a later time.'
                    }
                    $('.loader').remove();
                    $('.is_loading').remove();
                    $('#wrapper').html(msg);
                },
            })
        })
    }
})