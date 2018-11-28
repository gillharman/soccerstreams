function getMatchInfo(b) {
    var match_id = b.id;
    $.ajax({
        url: 'ajax/match_info',
        async: false,
        data: {
            'match_id': match_id
        },
        success: function(result) {
            $('#game_info').css('display', 'inline-block');
            if($('#game_info').children().length) {
                $('#game_info').children().remove();
            }
            $('#game_info').append(result);
            _setCardWidth();
        }
    });
}

function closeCard() {
    $('#game_info').children().remove();
    $('#game_info').css('display', 'none');
}

function _setCardWidth() {
    var parentWidth = $('#game_info').width();
    $('.card').width(parentWidth);
}

$(window).resize(function() {
    if($('#game_info').children().length) {
        var parentWidth = $('#game_info').width();
        $('.card').width(parentWidth);
    }
})