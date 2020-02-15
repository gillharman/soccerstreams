$(document).ready(function() {
    var links = $("#matchup-nav ul li");
    for (var i = 0; i < links.length; ++i) {
        $(links[i]).on("click", function() {
            $('ul li.tab-active').removeClass('tab-active');
            $('.tab-content').css('display', 'none');

            var tab_content = $(this).attr('data-tab-content');
            $('#' + tab_content).css('display','flex');
            $(this).addClass('tab-active');

            // Add last open tab to localStorage
            window.localStorage["lastOpenTab"] = this.id;
        });
    }

    $('#ace-stream-form form').on("submit", function(event) {
        $(".new-links-alert").hide();
        event.preventDefault();
        $(".progress-bar").animate({
            width: "100%",
        }, 800, function() {
            addAceStream();
            $(".progress-bar").css("width", "0");
        });
    });

    $('#add-another-ace-stream').on("click", function() {
        addAceStreamForm();
    });

    $('.content-id input').on("focus", function(ele) {
        if(!$(this).val()) {
            $(this).val("acestream://");
        }
    });

    $('.content-id input').on("blur", function(ele) {
        if($(this).val() === "acestream://") {
            $(this).val("");
        }
    });

    $('.close-alert').on("click", function() {
        $('.new-links-alert').hide();
    });

    // Activate the last open tab
    if(window.localStorage.lastOpenTab) {
        $("#" + window.localStorage.lastOpenTab).click();
    } else {
        $('#lineups-menu').click();
    }
});

function getCookie(name) {
    var cookieValue = null;
    if(document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for(var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // DOES THIS COOKIE STRING BEGIN WITH THE NAME WE WANT?
            if(cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // THESE HTTP METHODS DO NOT REQUIRE CSRF PROTECTION
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function addAceStream() {
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if(!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
        type: "POST",
        url: "/ajax/add_ace_stream",
        data: buildPostPackage(),
        success: function(result) {
            var new_links = JSON.parse(result.data.new_links);
            addLinksToDOM(new_links);
            $("#ace-stream-form").prepend(addToastMessage("success", result.data.inserts));
        },
        error: function() {
            $("#ace-stream-form").prepend(addToastMessage("failed"));
        },
    });
}

function buildPostPackage() {
    var data = {};
    data.match_id = $("input[name='match_id']").val();
    data.league = $("input[name='league']").val();
    data["form-TOTAL_FORMS"] = $("#id_form-TOTAL_FORMS").val();
    data["form-INITIAL_FORMS"] = $("#id_form-INITIAL_FORMS").val();
    data["form-MIN_NUM_FORMS"] = $("#id_form-MIN_NUM_FORMS").val();
    data["form-MAX_NUM_FORMS"] = $("#id_form-MAX_NUM_FORMS").val();
    for(var i=0; i<data["form-TOTAL_FORMS"]; ++i) {
        data["form-" + i + "-ace_stream"] = $("#id_form-" + i + "-ace_stream").val();
    }
    return data;
}

function addLinksToDOM(arr) {
    var link;
    for(var i=0; i != arr.length; ++i) {
        $("#acestreams .last-row").removeClass("last-row");
        var td = document.createElement("td");
        link = document.createTextNode(arr[i].fields.link);
        td.appendChild(link);

        var tr = document.createElement("tr");
        tr.appendChild(td);
        $("#acestreams table tbody").append(tr);
    }
    return;
}

function addAceStreamForm() {
    var num = incrementForms();
    num -= 1;  // IDS ARE INDEXED FROM ZERO
    var label_clone = $("label[for='id_form-0-ace_stream']").clone().attr({
        "for": "id_form-" + num + "-ace_stream",
    });
    var input_clone = $("#id_form-0-ace_stream").clone(true).attr({
        id: "id_form-" + num + "-ace_stream",
        name: "form-" + num + "-ace_stream",
    });

    // CLEAR VALUES FROM INPUT TEXT FIELD
    $(input_clone).val("");

    var new_content_id_html = document.createElement("div");
    new_content_id_html.classList.add("content-id");
    new_content_id_html.appendChild(label_clone[0]);
    new_content_id_html.appendChild(input_clone[0]);

    $("#content-ids").append(new_content_id_html);
    return;
}

function incrementForms() {
    var total_forms = Number($("#id_form-TOTAL_FORMS").val());
    total_forms += 1;
    $("#id_form-TOTAL_FORMS").val(total_forms);
    return total_forms;
}

function addToastMessage(type, arr) {
    if(arr != undefined && arr != '')
        arr = arr.join()
    else
        arr = ''
    var toast = {
        "success": {
            "message": "Success!",
            "classType": "alert alert-success"
        },
        "failed": {
            "message": "Error.",
            "classType": "alert alert-danger"
        }
    }

    if($(".new-links-alert").hasClass("alert")) {
        $(".new-links-alert").contents().first().remove();
    }
    $(".new-links-alert")
        .addClass(toast[type].classType)
        .prepend(toast[type].message)
        .show();

    return;
}