function clickPlus() {
    $("input[name=new-target]").fadeTo(500, 1);

}

function showError(message) {
    let subj = $(".error");
    subj.html(message);
    subj.fadeIn(300);
}

function hideError() {
    $(".error").fadeOut();
}

function showNewTarget() {
    $(".new-target").show();
    $(".container").hide();
}

function hideNewTarget() {
    $(".new-target").hide();
    $(".container").show();
}

function submitNewTarget() {
    let newTarget = $("#new-target-value").val();

    $.ajax({
        url: '/new-target/',
        method: "POST",
        data: {
            "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
            "newTarget": newTarget
        },
        success: function (data) {
            console.log("new target created:");
            console.log(data);
            hideNewTarget();
        },
        error: function (data) {
            showError(data.responseText);
            hideNewTarget();
        }
    })
}

function doPush() {
    let howMuch = parseInt($("#how-much").val());


    if (isNaN(howMuch)) {
        $(".error").html(now() + "Количество потраченных денег должно быть целым числом.");
    }
}

function now() {
    let now = new Date(),
        mins = now.getMinutes(),
        secs = now.getSeconds(),
        nows = now.getHours() + ":";
    if (mins < 10) {
        nows += "0" + mins;
    } else {
        nows += mins;
    }
    nows += ":";
    if (secs < 10) {
        nows += "0" + secs;
    } else {
        nows += secs;
    }

    return "[" + nows + "]: ";
}

function whoChanged() {
    let cid = parseInt($('#who-select').val());

    if (cid === -1) {

    }
}

function targetChanged() {
    let tid = parseInt($('#what-select').val());

    if (tid === -1) {
        showNewTarget();
    }
}

function loadFile() {
    $.ajax({
        url: "/load-file/"
    })
}