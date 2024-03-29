

function generateRandomHash(length) {
    var result = '';
    var characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}


$(document).on("click", "#gen-id", function (){ $("#id").val(generateRandomHash(20))})

$(document).on("click", "#take-attendance", function () {
    $("imaging-label").html("Taking Attendance")
    $('#imaging').modal('show');
    $.ajax({
        url: "/mark-attendance",
        type: "POST",
        contentType: "application/json; charset=UTF-8",
        success: function (response) {
            $('#imaging').modal('hide');
            if (response.message.indexOf('success') == -1) {
                Swal.fire({
                    icon: 'error',
                    text: response.data.message
                })
            } else {
                Swal.fire({
                    icon: 'success',
                    title: response.data.message
                })
            }
        }
    });
})

$(document).on("click", "#add-participant", function () {
    $("#submit-participant").attr('data-action', 'add')
    $("#id").prop('disabled', false);
})

$(document).on("click", "#submit-participant", function () {
    action = $("#submit-participant").attr('data-action')
    let formdata = {}
    formdata['id'] = $("#id").val()
    formdata['name'] = $("#name").val()
    formdata['group'] = $("#group").val()
    formdata['group'] = $("#group").val()
    formdata['action'] = action

    if (formdata['group']?.trim() != "" && formdata['id']?.trim() != "" && formdata['name']?.trim() != "") {
        if (action == "add") { $('#imaging').modal('show'); }
        else { $("#loading").addClass('load'); }

        $("imaging-label").html("Scanning Participant")
        $.ajax({
            url: `/action-participant`,
            type: "POST",
            data: JSON.stringify(formdata),
            contentType: "application/json; charset=UTF-8",
            success: function (response) {
                if (action == "add") { $('#imaging').modal('hide'); }
                else { $("#loading").removeClass('load'); }

                if (response.message.indexOf('success') == -1) {
                    Swal.fire({
                        icon: 'error',
                        text: response.data.message
                    })
                } else {
                    Swal.fire({
                        icon: 'success',
                        title: response.data.message,
                        showConfirmButton: false,
                        timer: 1000
                    }).then(function () {
                        window.location.reload();
                    })
                }
            }
        });
    }

})

$(document).on("click", ".del-participant", function () {
    participant_id = $(this).attr("data-id")
    $("#loading").addClass('load');
    $.ajax({
            url: `/del-participants?participant=${participant_id}`,
            type: "POST",
            contentType: "application/json; charset=UTF-8",
            success: function (response) {
                $('#loading').removeClass('load');
                if (response.message.indexOf('success') == -1) {
                    Swal.fire({
                        icon: 'error',
                        text: response.data.message
                    })
                } else {
                    Swal.fire({
                        icon: 'success',
                        title: response.data.message,
                        showConfirmButton: false,
                        timer: 1000
                    }).then(function () {window.location.reload();})
                }
            }
        });
})

$(document).on("click", ".update-participant", function () {
    participant_id = $(this).attr("data-id");

    $("#loading").addClass('load');
    $.ajax({
        url: `/get-participants?participant=${participant_id}`,
        type: "GET",
        contentType: "application/json; charset=UTF-8",
        success: function (response) {
            $('#loading').removeClass('load');
            if (response.message.indexOf('success') == -1) {
                Swal.fire({
                    icon: 'error',
                    text: response.data.message
                })
            } else {
                participant = response.data
                if (participant) {
                    $("#id").val(participant["id"])
                    $("#name").val(participant["name"])
                    $("#group").val(participant["group"])

                    $("#id").prop('disabled', true);
                    $("#participant-modal").modal('show');
                    $("#submit-participant").attr('data-action', 'update')
                }
                else{
                    Swal.fire({
                        icon: 'warning',
                        text: "No Participant Found"
                    })
                }
            }
        }
    });
})


