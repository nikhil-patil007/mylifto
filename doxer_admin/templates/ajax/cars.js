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

// AJAX FOR Car Accept : 
$(".accept-car").on('click',function(){
    var Page_num = $('.pagination li.page-item.active').index();
    var id = $(this).attr('data-sid');    
    $("#accept_car").text("Please Wait...."); 
    $('#accept_car').attr('disabled', 'disabled');
    var timedate = $("#pdate").text();
    mydata = {pid:id, 'date':timedate, 'csrfmiddlewaretoken': '{{ csrf_token }}','page_no':Page_num}
    mythis = this;
    $.ajax({
        url : "{% url 'doxer_admin:caraccept' %}",
        method : "POST",
        data : mydata,
        success : function(data){
            if (data.status==1){
                setTimeout(function() {
                    $('#Accept').modal('hide');
                    $('#accept_car').removeAttr('disabled');
                    $("#accept_car").text("Accept Car");
                }, 1000);
                setTimeout(function() {
                    var page_range = data.page_range;
                    $("#tests-table").attr('data-sid',+page_range);
                    $("#tests-table").attr('page_no',+Page_num);
                    var pass = data.results;
                    if (pass == "None"){
                        $("#"+id).fadeOut();
                    } else {
                        $('#tests-table').html('');
                        $.each(pass, function(i, val) {
                            //append to post
                            for(var j=1 ; j <= i ; j++){j};
                            if(val.status == '0'){
                                var status = "<label class='badge badge-info'>New</label>";
                            } else if(val.status == '1'){
                                var status = "<label class='badge badge-success'>Approval</label>";
                            } else if(val.status == '2'){
                                var status = "<label class='badge badge-danger'>Rejected</label>";
                            } else {
                                var status = '';
                            }
                            $('#tests-table').append("<tr id='"+val.id+"'><td class='123'> # " + val.id  + "</td><td>" + "<img src=" +val.pro_image + " alt='car_image' /><span class='pl-2'>" + val.driverid + "</span></td><td>"+ val.reg_num +"</td><td>"+ val.vehical_variant +"</td><td>" + val.vehicle_color + "</td><td>"+ status + "</td><td>" +
                                "<button class='btn btn-success btn-rounded btn-sm Accept-ca' data-target='#Accept' data-toggle='modal' data-sid='"+val.id+"'> <i class='icon-check btn-icon-append'></i></button>  <button class='btn btn-danger btn-rounded  btn-sm Reject-ca' data-target='#Reject' data-toggle='modal' data-sid='"+val.id+"'><i class='icon-close btn-icon-append'></i></button>"
                                + '</td></tr>')
                            });
                        }
                        $("#et1").text(data.a);
                        $("#et2").text(data.b);
                        $("#totale").text(data.t);
                    }, 2000);
                }
                if (data.status==0){
                setTimeout(function() {
                    $('#Accept').modal('hide');
                    $('#accept_car').removeAttr('disabled');
                    $("#accept_car").text("Accept Car");
                }, 1000);
            }
        },
    });
});

// AJAX FOR Car Reject : 
$(".reject-car").on('click',function(){
    var id = $(this).attr('data-sid');    
    var Page_num = $('.pagination li.page-item.active').index();
    $("#reject_car").text("Please Wait...."); 
    $('#reject_car').attr('disabled', 'disabled');
     var timedate = $("#pdate").text();
    mydata = {pid:id, 'date':timedate, 'csrfmiddlewaretoken': '{{ csrf_token }}','page_no':Page_num}
    mythis = this;
    $.ajax({
        url : "{% url 'doxer_admin:carreject' %}",
        method : "POST",
        data : mydata,
        success : function(data){
            if (data.status==1){
                setTimeout(function() {
                    $('#Reject').modal('hide');
                    $('#reject_car').removeAttr('disabled');
                    $("#reject_car").text("Reject Car");
                }, 1000);
                setTimeout(function() {
                    var page_range = data.page_range;
                    $("#tests-table").attr('data-sid',+page_range);
                    $("#tests-table").attr('page_no',+Page_num);
                    var pass = data.results;
                    if (pass == "None"){
                        $("#"+id).fadeOut();
                    } else {
                        $('#tests-table').html('');
                        $.each(pass, function(i, val) {
                            //append to post
                            for(var j=1 ; j <= i ; j++){j};
                            if(val.status == '0'){
                                var status = "<label class='badge badge-info'>New</label>";
                            } else if(val.status == '1'){
                                var status = "<label class='badge badge-success'>Approval</label>";
                            } else if(val.status == '2'){
                                var status = "<label class='badge badge-danger'>Rejected</label>";
                            } else {
                                var status = '';
                            }
                        $('#tests-table').append("<tr id='"+val.id+"'><td class='123'> # " + val.id  + "</td><td>" + "<img src=" +val.pro_image + " alt='car_image' /><span class='pl-2'>" + val.driverid + "</span></td><td>"+ val.reg_num +"</td><td>"+ val.vehical_variant +"</td><td>" + val.vehicle_color + "</td><td>"+ status + "</td><td>" +
                            "<button class='btn btn-success btn-rounded btn-sm Accept-ca' data-target='#Accept' data-toggle='modal' data-sid='"+val.id+"'> <i class='icon-check btn-icon-append'></i></button>  <button class='btn btn-danger btn-rounded  btn-sm Reject-ca' data-target='#Reject' data-toggle='modal' data-sid='"+val.id+"'><i class='icon-close btn-icon-append'></i></button>"
                            + '</td></tr>')
                        });
                    }
                    $("#et1").text(data.a);
                    $("#et2").text(data.b);
                    $("#totale").text(data.t);
                }, 2000);
            }
            if (data.status==0){
                setTimeout(function() {
                    $('#Reject').modal('hide');
                    $('#reject_car').removeAttr('disabled');
                    $("#reject_car").text("Reject Car");
                }, 1000);
            }
        },
    });
});

$('tbody').on('click','.Accept-ca',function(){
    let id = $(this).attr('data-sid');
    mydata = {pid:id, 'csrfmiddlewaretoken': '{{ csrf_token }}'}
    mythis = this;
    $.ajax({
        url : "{% url 'doxer_admin:editcar' %}",
        method : "POST",
        data : mydata,
        dataType : "json",
        success : function(data){
            $('#title_car').text(data.car);
            $("#accept_car").attr('data-sid',data.id);
        },
    });
});

$('tbody').on('click','.Reject-ca',function(){
    let id = $(this).attr('data-sid');
    mydata = {pid:id, 'csrfmiddlewaretoken': '{{ csrf_token }}'}
    mythis = this;
    $.ajax({
        url : "{% url 'doxer_admin:editcar' %}",
        method : "POST",
        data : mydata,
        dataType : "json",
        success : function(data){
            $('#title_car2').text(data.car);
            $("#reject_car").attr('data-sid',data.id);
        },
    });
});

$('.pagination li.page-item').on('click',function(){
    var data = $(this).attr('data');
    if ($(this).hasClass('active')){
        return false;
    } else {
        var currentpage = $(this).index();
        var page_no = currentpage;
        $('.pagination li').removeClass('active');
        $(this).addClass('active');
        $('.pagination a').removeClass('btn-info').addClass('btn-primary');
        $('li.page-item.active a').removeClass('btn-primary').addClass('btn-info');
        $('#tests-table').html('');
        $('#tests-table').append("<tr><th colspan=8><center><div class='spinner-border' role='status'></div></center></th></tr>");
        $.ajax({
            type: "POST",
            // define url name
            url: "{% url 'doxer_admin:allcars' %}", 
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
                        if(val.status == '0'){
                            var status = "<label class='badge badge-info'>New</label>";
                        } else if(val.status == '1'){
                            var status = "<label class='badge badge-success'>Approval</label>";
                        } else if(val.status == '2'){
                            var status = "<label class='badge badge-danger'>Rejected</label>";
                        } else {
                            var status = '';
                        }
                        $('#tests-table').append("<tr id='"+val.id+"'><td class='123'> # " + val.id  + "</td><td>"+ val.date +"</td><td>" + "<img src=" +val.pro_image + " alt='car_image' /><span class='pl-2'>" + val.driverid + "</span></td><td>"+ val.reg_num +"</td><td>"+ val.vehical_variant +"</td><td>" + val.vehicle_color + "</td><td>"+ status + "</td><td>" +
                            "<button class='btn btn-success btn-rounded btn-sm Accept-ca' data-target='#Accept' data-toggle='modal' data-sid='"+val.id+"'> <i class='icon-check btn-icon-append'></i></button>  <button class='btn btn-danger btn-rounded  btn-sm Reject-ca' data-target='#Reject' data-toggle='modal' data-sid='"+val.id+"'><i class='icon-close btn-icon-append'></i></button>"
                            + '</td></tr>')
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
        $('#tests-table').html('');
        $('#tests-table').append("<tr><th colspan=8><center><div class='spinner-border' role='status'></div></center></th></tr>");
        $("#next-page").removeAttr('disabled');
        $("#prev-page").removeAttr('disabled');
        var currentpage = $('.pagination li.active').index();
        var nextpage = currentpage + 1;
        $.ajax({
            type: "POST",
            // define url name
            url: "{% url 'doxer_admin:allcars' %}", 
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
                        
                        if(val.status == '0'){
                            var status = "<label class='badge badge-info'>New</label>";
                        } else if(val.status == '1'){
                            var status = "<label class='badge badge-success'>Approval</label>";
                        } else if(val.status == '2'){
                            var status = "<label class='badge badge-danger'>Rejected</label>";
                        } else {
                            var status = '';
                        }
                        $('#tests-table').append("<tr id='"+val.id+"'><td class='123'> # " + val.id  + "</td><td>"+ val.date +"</td><td>" + "<img src=" +val.pro_image + " alt='car_image' /><span class='pl-2'>" + val.driverid + "</span></td><td>"+ val.reg_num +"</td><td>"+ val.vehical_variant +"</td><td>" + val.vehicle_color + "</td><td>"+ status + "</td><td>" +
                            "<button class='btn btn-success btn-rounded btn-sm Accept-ca' data-target='#Accept' data-toggle='modal' data-sid='"+val.id+"'> <i class='icon-check btn-icon-append'></i></button>  <button class='btn btn-danger btn-rounded  btn-sm Reject-ca' data-target='#Reject' data-toggle='modal' data-sid='"+val.id+"'><i class='icon-close btn-icon-append'></i></button>"
                            + '</td></tr>')
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
        $('#tests-table').html('');
        $('#tests-table').append("<tr><th colspan=8><center><div class='spinner-border' role='status'></div></center></th></tr>");
        $("#prev-page").removeAttr('disabled');
        $("#next-page").removeAttr('disabled');
        var currentpage = $('.pagination li.active').index();
        var nextpage = currentpage - 1;
        $.ajax({
            type: "POST",
            // define url name
            url: "{% url 'doxer_admin:allcars' %}", 
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
                        
                        if(val.status == '0'){
                            var status = "<label class='badge badge-info'>New</label>";
                        } else if(val.status == '1'){
                            var status = "<label class='badge badge-success'>Approval</label>";
                        } else if(val.status == '2'){
                            var status = "<label class='badge badge-danger'>Rejected</label>";
                        } else {
                            var status = '';
                        }
                        $('#tests-table').append("<tr id='"+val.id+"'><td class='123'> # " + val.id  + "</td><td>"+ val.date +"</td><td>" + "<img src=" +val.pro_image + " alt='car_image' /><span class='pl-2'>" + val.driverid + "</span></td><td>"+ val.reg_num +"</td><td>"+ val.vehical_variant +"</td><td>" + val.vehicle_color + "</td><td>"+ status + "</td><td>" +
                            "<button class='btn btn-success btn-rounded btn-sm Accept-ca' data-target='#Accept' data-toggle='modal' data-sid='"+val.id+"'> <i class='icon-check btn-icon-append'></i></button>  <button class='btn btn-danger btn-rounded  btn-sm Reject-ca' data-target='#Reject' data-toggle='modal' data-sid='"+val.id+"'><i class='icon-close btn-icon-append'></i></button>"
                            + '</td></tr>')
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
    $('#tests-table').append("<tr><th colspan=8><center><div class='spinner-border' role='status'></div></center></th></tr>");
    $.ajax({
        type: "POST",
        url: "{% url 'doxer_admin:allcars' %}", 
        data : {'page_no' : page_no, csrfmiddlewaretoken: '{{ csrf_token }}'},
        // handle a successful response
        success: function (data) {
            $("#et1").text(data.a);
            $("#et2").text(data.b);
            $("#totale").text(data.t);
            if (data.results == ''){
                $('#tests-table').html('');
                $('#tests-table').append("<tr><th colspan=8><center>No Records</center></th></tr>");
            } else {
                $('#tests-table').html('');
                $('.pagination ').fadeIn();
                $.each(data.results, function(i, val) {
                    //append to post
                    for(var j=1 ; j <= i ; j++){j};
                    
                    if(val.status == '0'){
                        var status = "<label class='badge badge-info'>New</label>";
                    } else if(val.status == '1'){
                        var status = "<label class='badge badge-success'>Approval</label>";
                    } else if(val.status == '2'){
                        var status = "<label class='badge badge-danger'>Rejected</label>";
                    } else {
                        var status = '';
                    }
                    $('#tests-table').append("<tr id='"+val.id+"'><td class='123'> # " + val.id  + "</td><td>"+ val.date +"</td><td>" + "<img src=" +val.pro_image + " alt='car_image' /><span class='pl-2'>" + val.driverid + "</span></td><td>"+ val.reg_num +"</td><td>"+ val.vehical_variant +"</td><td>" + val.vehicle_color + "</td><td>"+ status + "</td><td>" +
                        "<button class='btn btn-success btn-rounded btn-sm Accept-ca' data-target='#Accept' data-toggle='modal' data-sid='"+val.id+"'> <i class='icon-check btn-icon-append'></i></button>  <button class='btn btn-danger btn-rounded  btn-sm Reject-ca' data-target='#Reject' data-toggle='modal' data-sid='"+val.id+"'><i class='icon-close btn-icon-append'></i></button>"
                        + '</td></tr>')
                    });
                }
            },
            error: function () {
                alert('Page Not Founded');
            }
    }); 
});

