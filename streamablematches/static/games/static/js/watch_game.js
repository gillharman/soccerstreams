$(document).ready(function() {
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

    $('#ace-stream-form form').on("submit", function(event) {
        event.preventDefault();
        addAceStream();
    });

    $('#add-another-ace-stream').on("click", function() {
        addAceStreamForm();
    });

    $('.content-id input').on("focus", function(ele) {
        if(!$(this).val()) {
            $(this).val("acestream://");
        }
    });

    // ACTIVATE THE LINEUPS TAB
    $('#default-open').click();
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
            if(result.data.ignored.length > 0)
                $("#ace-stream-form").prepend(addToastMessage("failed", result.data.ignored));
            if(result.data.inserts.length > 0)
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
        for: "form-" + num + "-ace_stream",
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
            "message": "Links added successfully!" + arr,
            "classType": "success"
        },
        "failed": {
            "message": "An error occurred while adding new links. " + arr,
            "classType": "danger"
        }
    }
    var div_tag = document.createElement("div");
    $(div_tag).attr({
        "class": "alert alert-" + toast[type].classType,
        "role": "alert"
    });
    var message_node = document.createTextNode(toast[type].message);
    div_tag.appendChild(message_node);

    return div_tag;
}