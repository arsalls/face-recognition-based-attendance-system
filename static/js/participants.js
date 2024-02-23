

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
                    title: response.data.message,
                    timer: 1000
                })
            }
        }
    });
})

$(document).on("click", "#submit-participant", function () {
    let formdata = {}
    formdata['id'] = $("#id").val()
    formdata['name'] = $("#name").val()
    formdata['group'] = $("#group").val()

    if (formdata['group']?.trim() != "" && formdata['id']?.trim() != "" && formdata['name']?.trim() != "") {
        $('#imaging').modal('show');
        $("imaging-label").html("Scanning Participant")
        $.ajax({
            url: "/add-participants",
            type: "POST",
            data: JSON.stringify(formdata),
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


