function d_getMatchInfo(b) {
    var matchId = b.value.replace("btn_", "");
    var isMobile = _isMobile();
    getMatchInfo(matchId, isMobile);
}

function m_getMatchInfo(b) {
    var matchId = b.value.replace("mobileBtn_", "");
    var isMobile = _isMobile();
    if($("#gameInfo_" + matchId).hasClass("displayed")) {
        _toggleCard(matchId);
    } else {
        getMatchInfo(matchId, isMobile);
    }
}

function getMatchInfo(match_id, isMobile) {
    $.ajax({
        url: 'ajax/match_info',
        async: false,
        data: {
            'match_id': match_id
        },
        success: function(result) {
            if(isMobile) {
                displayMobile(result, match_id);
            } else {
                displayDesktop(result);
            }
        }
    });
}

function displayDesktop(result) {
    //FORMAT CARD
    var scrollTop = $(window).scrollTop();
    $('#game_info').css('margin-top', scrollTop);
    $('#game_info').removeClass('game-info-hidden');
    $('#game_info').addClass('game-info-displayed');

    if($('#game_info').children().length) {
        $('#game_info').children().remove();
    }
    $('#game_info').append(result);
}

function displayMobile(result, element_id) {
    var ele = $("#gameInfo_" + element_id);
    if(ele.children().length) {
        ele.children().remove();
    }
    ele.append(result);
    ele.collapse('toggle');
    ele.addClass('displayed');
}

function closeCard(b) {
    var isMobile = _isMobile();
    if(isMobile) {
        var match_id = b.value.replace("closeBtn_", "");
        _toggleCard(match_id);
    } else {
        $('#game_info').children().remove();
        $('#game_info').addClass('game-info-hidden');
        $('#game_info').removeClass('game-info-displayed');
    }
}

function _isMobile() {
    return ($("#isMobile").val() == "True");;
}

function _toggleCard(matchId) {
    $("#gameInfo_" + matchId).collapse("toggle");
    $("#gameInfo_" + matchId).removeClass("displayed");
}