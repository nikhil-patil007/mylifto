$(document).ready(function() {
    mydata = { 'pid': '1', 'csrfmiddlewaretoken': '{{ csrf_token }}' }
    mythis = this;
    $.ajax({
        url: 'index/', //"{% url 'doxer_admin:indexpage' %}",
        method: "POST",
        data: mydata,
        success: function(data) {
            if (data.sess == "1") {
                setInterval(function() {
                    $("#spinnereupdate").removeClass('spinner-grow text-danger');
                    $("#spinnereupdate").addClass('spinner-grow text-success');
                }, 800);
                // console.log(data);
                if (data.income == 'None') {
                    $('#income').html('');
                    $('#income').append("₹ 00.0");
                } else {
                    $('#income').html('');
                    $('#income').append("₹ " + data.income);
                }
                $('#hrdri').text(data.dri);
                $('#h4pas').text(data.pas);

                if (data.today == 'None') {
                    $('#h4today').html('');
                    $('#h4today').append("₹ 00.0");
                } else {
                    $('#h4today').html('');
                    $('#h4today').append("₹ " + data.today);
                }
                if (data.dri1 >= 1) {
                    $('#orspan').html('');
                    $('#spandri').html('');
                    $('#spandri').append(+data.dri1 + ' Block');
                } else {
                    $('#orspan').html('');
                    $('#spandri').html('');
                    $('#spandri').append("&nbsp; ");
                }

                if (data.pas1 >= 1) {
                    $('#orspan2').html('');
                    $('#spanpas').html('');
                    $('#spanpas').append(+data.pas1 + ' Block');
                } else {
                    $('#orspan2').html('');
                    $('#spanpas').html('');
                    $('#spanpas').append("&nbsp; ");
                }
                var refreshIntervalId = setInterval(ajaxCall, 1000);
            } else {
                window.location.assign("/doxer-admin");
            }
        },
    });
});

function ajaxCall() {
    $.ajax({
        url: 'index/', //"{% url 'doxer_admin:indexpage' %}",
        method: "POST",
        data: mydata,
        success: function(data) {
            if (data.sess == '1') {
                setInterval(function() {
                    $("#spinnereupdate").removeClass('spinner-grow text-success');
                    $("#spinnereupdate").addClass('spinner-grow text-danger');
                    setInterval(function() {
                        $("#spinnereupdate").removeClass('spinner-grow text-danger');
                        $("#spinnereupdate").addClass('spinner-grow text-success');
                    }, 500);
                }, 800);
                // console.log(data);
                if (data.income == 'None') {
                    $('#income').html('');
                    $('#income').append("₹ 00.0");
                } else {
                    $('#income').html('');
                    $('#income').append("₹ " + data.income);
                }
                $('#hrdri').text(data.dri);
                $('#h4pas').text(data.pas);

                if (data.today == 'None') {
                    $('#h4today').html('');
                    $('#h4today').append("₹ 00.0");
                } else {
                    $('#h4today').html('');
                    $('#h4today').append("₹ " + data.today);
                }
                if (data.dri1 >= 1) {
                    $('#orspan').html('');
                    $('#spandri').html('');
                    $('#spandri').append(+data.dri1 + ' Block');
                } else {
                    $('#orspan').html('');
                    $('#spandri').html('');
                    $('#spandri').append("&nbsp; ");
                }

                if (data.pas1 >= 1) {
                    $('#orspan2').html('');
                    $('#spanpas').html('');
                    $('#spanpas').append(+data.pas1 + ' Block');
                } else {
                    $('#orspan2').html('');
                    $('#spanpas').html('');
                    $('#spanpas').append("&nbsp; ");
                }
            } else {
                window.location.assign("/doxer-admin");
            }
        },
    });
}