// Show First Page Num of Button on Front end
var endofpage = '{{pages}}';
if (endofpage > 1){
    $(".pagination").append("<li><button class='btn btn-sm btn-primary btn-rounded' id='prev-page' href='javascript:void(0)' disabled>Previous</button>&nbsp;</li><li class='page-item active' hidden><a class='btn btn-info btn-rounded btn-sm' href='javascript:void(0)' data=1>" + 1 + "</a>&nbsp;</li>");
}

if(endofpage >= 2){
    // For Check Current Index
    var currentindex = $('.pagination li.active').index();
    
    // Show Num of Pages Button on Front end
    for (var i = 2 ;i <= endofpage; i++){
        $(".pagination").append("<li class='page-item' hidden><a class='btn btn-primary btn-rounded btn-sm' href='javascript:void(0)' data="+ i +">" + i + "</a>&nbsp;</li>");
    }
    
    // Show Next Button on Front end
    $(".pagination").append("<li>&nbsp;<button class='btn-sm btn btn-primary btn-rounded' id='next-page' href='javascript:void(0)' data=''>" + 'Next' + "</button></li>");
}

$('.pagination li.page-item').on('click',function(){
    var data = $(this).attr('data');
    if ($(this).hasClass('active')){
        return false;
    } else {
        $('#tests-table').html('');
        $('#tests-table').append("<tr><th colspan=10><center><div class='spinner-border' role='status'></div></center></th></tr>");
        var currentpage = $(this).index();
        var page_no = currentpage;

        $('.pagination li').removeClass('active');
        $(this).addClass('active');
        $('.pagination a').removeClass('btn-info').addClass('btn-primary');
        $('li.page-item.active a').removeClass('btn-primary').addClass('btn-info');
        
        $.ajax({
            type: "POST",
            // define url name
            url: "{% url 'doxer_admin:allrides' %}", 
            data : {    
                page_no : page_no, 
                csrfmiddlewaretoken: '{{ csrf_token }}',
            },
            // handle a successful response
            success: function (data) {
                if ($(this).hasClass('active')){
                    return false;
                } else {
                    $('#tests-table').html('');
                    $("#et1").text(data.a);
                    $("#et2").text(data.b);
                    $("#totale").text(data.t);
                    $.each(data.results, function(i, val) {
                        //append to post
                        for(var j=1 ; j <= i ; j++){j};
                        if(val.str == "1"){
                            console.log('1');
                            var tr = "table-danger";
                        }else{
                            console.log('0');
                            var tr = "";
                        }
                        $('#tests-table').append("<tr class='"+ tr +"'><td> # " + val.id  + "</td><td>" + val.trip_date + "<br><br>"+val.ride_time+"</td><td>"+ val.create_at +"</td><td>" + val.getdr + "</td><td>"+ val.getpas +"</td><td>"+ val.vehicle +"</td><td>" + val.Location + "<br><br>" + val.destination + "</td><td><center>"+ val.status +"</center></td><th>  "+ val.fees + "</th><td><center><button class='btn btn-success btn-rounded btn-sm' id='pleaseclickme' data='"+val.rid+"'><i class='icon-direction btn-icon-append'></i></button></td></tr>")
                        });
                    };
                },
                error: function () {
                    alert('Page Not Founded');
                }
            }); 
        }
});

$("#next-page").on('click',function(){
    var currentpage = $('.pagination li.active').index();
    if (currentpage == endofpage){
        $("#next-page").attr('disabled','True');
    }else{
        $("#next-page").removeAttr('disabled');
        $("#prev-page").removeAttr('disabled');
        var currentpage = $('.pagination li.active').index();
        var nextpage = currentpage + 1;
        $('#tests-table').html('');
        $('#tests-table').append("<tr><th colspan=10><center><div class='spinner-border' role='status'></div></center></th></tr>");
        $.ajax({
            type: "POST",
            // define url name
            url: "{% url 'doxer_admin:allrides' %}", 
            data : {    
                page_no : nextpage, 
                csrfmiddlewaretoken: '{{ csrf_token }}',
            },
            // handle a successful response
            success: function (data) {
                if ($(this).hasClass('active')){
                    return false;
                } else {
                    $('.pagination li').removeClass('active');
                    $('#tests-table').html('');
                    $("#et1").text(data.a);
                    $("#et2").text(data.b);
                    $("#totale").text(data.t);
                    $.each(data.results, function(i, val) {
                        //append to post
                        for(var j=1 ; j <= i ; j++){j};
                        if(val.str == "1"){
                            console.log('1');
                            var tr = "table-danger";
                        }else{
                            console.log('0');
                            var tr = "";
                        }
                        $('#tests-table').append("<tr class='"+ tr +"'><td> # " + val.id  + "</td><td>" + val.trip_date + "<br><br>"+val.ride_time+"</td><td>"+ val.create_at +"</td><td>" + val.getdr + "</td><td>"+ val.getpas +"</td><td>"+ val.vehicle +"</td><td>" + val.Location + "<br><br>" + val.destination + "</td><td><center>"+ val.status +"</center></td><th>  "+ val.fees + "</th><td><center><button class='btn btn-success btn-rounded btn-sm' id='pleaseclickme' data='"+val.rid+"'><i class='icon-direction btn-icon-append'></i></button></td></tr>")
                        });
                    $(".pagination li.page-item:eq(" + (nextpage - 1 ) + ")").addClass('active');
                    $('.pagination a').removeClass('btn-info').addClass('btn-primary');
                    $('li.page-item.active a').removeClass('btn-primary').addClass('btn-info');
                    if ($('.pagination li.active').index() == endofpage){
                        $("#next-page").attr('disabled','True');
                    }
                };
            },
            error: function () {
                return false;
            }
        }); 
    }
});

$("#prev-page").on('click',function(){
    var currentpage = $('.pagination li.active').index();
    if (currentpage === 1){
        $("#prev-page").attr('disabled','True');
    }else{
        $("#prev-page").removeAttr('disabled');
        $("#next-page").removeAttr('disabled');
        var currentpage = $('.pagination li.active').index();
        var nextpage = currentpage - 1;
        $('#tests-table').html('');
        $('#tests-table').append("<tr><th colspan=10><center><div class='spinner-border' role='status'></div></center></th></tr>");
        $.ajax({
            type: "POST",
            // define url name
            url: "{% url 'doxer_admin:allrides' %}", 
            data : {    
                page_no : nextpage, 
                csrfmiddlewaretoken: '{{ csrf_token }}',
            },
            // handle a successful response
            success: function (data) {
                if ($(this).hasClass('active')){
                    return false;
                } else {
                    $('.pagination li').removeClass('active');
                    $('#tests-table').html('');
                    $("#et1").text(data.a);
                    $("#et2").text(data.b);
                    $("#totale").text(data.t);
                    $.each(data.results, function(i, val) {
                        //append to post
                        for(var j=1 ; j <= i ; j++){j};
                        if(val.str == "1"){
                            console.log('1');
                            var tr = "table-danger";
                        }else{
                            console.log('0');
                            var tr = "";
                        }
                        $('#tests-table').append("<tr class='"+ tr +"'><td> # " + val.id  + "</td><td>" + val.trip_date + "<br><br>"+val.ride_time+"</td><td>"+ val.create_at +"</td><td>" + val.getdr + "</td><td>"+ val.getpas +"</td><td>"+ val.vehicle +"</td><td>" + val.Location + "<br><br>" + val.destination + "</td><td><center>"+ val.status +"</center></td><th>  "+ val.fees + "</th><td><center><button class='btn btn-success btn-rounded btn-sm' id='pleaseclickme' data='"+val.rid+"'><i class='icon-direction btn-icon-append'></i></button></td></tr>")
                        });
                    $(".pagination li.page-item:eq(" + (nextpage - 1 ) + ")").addClass('active');
                    $('.pagination a').removeClass('btn-info').addClass('btn-primary');
                    $('li.page-item.active a').removeClass('btn-primary').addClass('btn-info');
                    if($('.pagination li.active').index() === 1){
                        $("#prev-page").attr('disabled','True');
                    }
                    };
                },
            error: function () {
                return false;
            }
        }); 
    }
});

$(document).ready(function(){
    var page_no = 1;
    $('#tests-table').html('');
    $('#tests-table').append("<tr><th colspan=10><center><div class='spinner-border' role='status'></div></center></th></tr>");
    $.ajax({
        type: "POST",
        url: "{% url 'doxer_admin:allrides' %}", 
        data : {'page_no' : page_no, csrfmiddlewaretoken: '{{ csrf_token }}'},
        // handle a successful response
        success: function (data) {
            console.log(data);
            console.log(data.results);
            if (data.results == ''){
                $('#tests-table').html('');
                $("#et1").text("0");
                $("#et2").text(data.b);
                $("#totale").text(data.t);
                $('#tests-table').append("<tr><th colspan=10><center>No Records</center></th></tr>");
            } else {
                $('#tests-table').html('');
                $("#et1").text(data.a);
                $("#et2").text(data.b);
                $("#totale").text(data.t);
                $('.pagination ').fadeIn();
                $.each(data.results, function(i, val) {
                    //append to post
                    if(val.str == "1"){
                        console.log('1');
                        var tr = "table-danger";
                    }else{
                        console.log('0');
                        var tr = "";
                    }                    
                    $('#tests-table').append("<tr class='"+ tr +"'><td> # " + val.id  + "</td><td>" + val.trip_date + "<br><br>"+val.ride_time+"</td><td>"+ val.create_at +"</td><td>" + val.getdr + "</td><td>"+ val.getpas +"</td><td>"+ val.vehicle +"</td><td>" + val.Location + "<br><br>" + val.destination + "</td><td><center>"+ val.status +"</center></td><th>  "+ val.fees + "</th><td><center><button class='btn btn-success btn-rounded btn-sm' id='pleaseclickme' data='"+val.rid+"'><i class='icon-direction btn-icon-append'></i></button></td></tr>")
                    });
                    for(var j=1 ; j <= i ; j++){j};
                }
            },
            error: function () {
                $('#tests-table').append("<tr><th colspan=9><center>No Records</center></th></tr>");
            }
    }); 
});

$(document).on('click','#pleaseclickme',function(){
   var Id = $(this).attr('data');
   $.ajax({
        type: "POST",
        url: "{% url 'doxer_admin:mapview' %}", 
        data : {'id' : Id, csrfmiddlewaretoken: '{{ csrf_token }}'},
        // handle a successful response
        success: function (data) {
            $("#id-lat-a").val(data.lat);
            $("#id-long-a").val(data.lng);
            $("#id-lat-b").val(data.lat_a);
            $("#id-long-b").val(data.lng_a);
            $("#id-rid-a").val(data.rid);
        }
   });
});
