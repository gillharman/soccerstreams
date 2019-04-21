$(document).ready(function() {

    $("#matchup-league").click(function() {
        window.location = "/";
    })

    var links = $("#matchup-nav ul li");
    for (var i = 0; i < links.length; ++i) {
        $(links[i]).on("click", function() {
            $('ul li.tab-active').removeClass('tab-active');
            $('.tab-content').css('display', 'none');

            var tab_content = $(this).attr('data-tab-content');
            $('#' + tab_content).css('display','flex');
            $(this).addClass('tab-active');
        });
    }

    $('#add-ace-stream').on("click", function() {
        $("#ace-stream-form").css("display", "inline-block");
    });


    // ACTIVATE THE LINEUPS TAB
    $('#default-open').click();
});