
$(document).on("click", "#login", function () {
    let formdata = {}
    formdata['email'] = $("#email").val()
    formdata['password'] = $("#password").val()

    if (formdata['username']?.trim() != "" && formdata['password']?.trim() != "") {
        $("#loading").addClass('load');
        $.ajax({
            url: "/login",
            type: "POST",
            data: JSON.stringify(formdata),
            contentType: "application/json; charset=UTF-8",
            success: function (response) {
                $("#loading").removeClass('load');
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
                    }).then(function () { window.location.replace("/"); })
                }
            }
        });
    }

})

$(document).on("click", "#register", function () {
    let formdata = {}
    formdata['name'] = $("#name").val()
    formdata['email'] = $("#email").val()
    formdata['password'] = $("#password").val()

    if (formdata['email']?.trim() != "" && formdata['password']?.trim() != "" && formdata['name']?.trim() != "") {
        $("#loading").addClass('load');
        $.ajax({
            url: "/register",
            type: "POST",
            data: JSON.stringify(formdata),
            contentType: "application/json; charset=UTF-8",
            success: function (response) {
                $("#loading").removeClass('load');
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
                }).then(function () {window.location.replace("/");})
                }
            }
        });
    }

})


