
$(document).ready(function () {
    let fromDateFormatted = formatDate( new Date())
    let dateObj = {
             startDateTime: fromDateFormatted,
             endDateTime: fromDateFormatted,
        };
    getAttendances(dateObj)

    $('#submitReportBtn').click(function() {
        // Get the values of 'From' and 'To' dates
        let fromDate = $('#fromDate').val();
        let toDate = $('#toDate').val();
            if (fromDate && toDate) {
            // Format the dates as 'MM/DD/YY'
            // Format the dates as 'MM/DD/YY'
            let fromDateFormatted = formatDate(fromDate);
            let toDateFormatted = formatDate(toDate);

            // Create an object to store the formatted dates
            let dateObj = {
                startDateTime: fromDateFormatted,
                endDateTime: toDateFormatted
            };
            getAttendances(dateObj)
        } else {
            // Display an alert message if either date is not selected
              toastr.error('Please select "From" or "To" date.')
        }


    });
    function formatDate(dateString) {
        var date = new Date(dateString);
        var month = date.getMonth() + 1;
        var day = date.getDate();
        var year = date.getFullYear().toString().slice(-2); // Get last two digits of the year

        // Pad single digits with leading zero
        if (month < 10) month = '0' + month;
        if (day < 10) day = '0' + day;

        return month + '/' + day + '/' + year;
    }
});

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
                    showCancelButton: false, // Hide the cancel button
                    confirmButtonText: 'OK' // Change the confirmation button text
                }).then((result) => {
                        location.reload();
                });

            }
        }
    });
})

function getAttendances(dateObj) {
    $("#generateReportBtn").attr("href",`/generate-attendance?startDateTime=${dateObj.startDateTime}&endDateTime=${dateObj.endDateTime}`)
    $.ajax({
        url: '/get_attendances', // Replace with the URL of the API you want to call
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(dateObj),
        success: function (data) {
            console.log("get attendances " , data)
            tbody = '#attendances-tbody'
             $(tbody).empty()
             let count=0
             for (let attendance in data.data) {
                 count=count+1
                 console.log(" let attendance " , data.data[attendance])
                    var append_add = `
                    <tr>
                        <td>${count}</td>
                        <td>${data.data[attendance].name}</td>
                         <td>${data.data[attendance].group}</td>
                         <td>${data.data[attendance].mark_date}</td>
                         <td>${data.data[attendance].mark_time}</td>
                    </tr>`
                 $(tbody).append(append_add);
             }

        }
        , error: function (xhr, status, error) {
            // Handle any errors that occur during the request
            console.error(error);
        }
    });

}




