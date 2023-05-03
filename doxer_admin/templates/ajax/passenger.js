// Blocke And Unblock Passenger

$('tbody').on('click','.check-block',function(){
    var id = $(this).attr('data-sid');
    mydata = {pid:id, 'csrfmiddlewaretoken': '{{ csrf_token }}'}
    mythis = this;
    $.ajax({
        url : "{% url 'doxer_admin:blockpas' %}",
        method : "POST",
        data : mydata,
        success : function(data){
            if (data.status==1){
                $('#'+id).html('');
                $('#'+id).append("<div class='onoffswitch'><input type='checkbox' name='onoffswitch' data-sid='" +id+ "' class='check-block onoffswitch-checkbox' id='myonoffswitch"+id+"'><label class='onoffswitch-label' for='myonoffswitch"+id+"'><div class='onoffswitch-inner'></div><div class='onoffswitch-switch'></div></label></div>");
            }
            if (data.status==2){
                $('#'+id).html('');
                $('#'+id).append("<div class='onoffswitch'><input type='checkbox' name='onoffswitch' data-sid='" +id+ "' class='check-block onoffswitch-checkbox' id='myonoffswitch"+id+"' checked><label class='onoffswitch-label' for='myonoffswitch"+id+"'><div class='onoffswitch-inner'></div><div class='onoffswitch-switch'></div></label></div>");
            }
            if (data.status==0){
                // console.log("Unable To Block")
            }
        },
    });
});


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
        $('#tests-table').append("<tr><th colspan=9><center><div class='spinner-border' role='status'></div></center></th></tr>");
        var currentpage = $(this).index();
        var page_no = currentpage;
        if (page_no == '1'){
            $("#prev-page").attr('disabled','True');
        } else {
            $("#prev-page").removeAttr('disabled');
        }
        if (currentpage == endofpage){
            $("#next-page").attr('disabled','True');
        }else{
            $("#next-page").removeAttr('disabled');
        }
        $('.pagination li').removeClass('active');
        $(this).addClass('active');
        $('.pagination a').removeClass('btn-info').addClass('btn-primary');
        $('li.page-item.active a').removeClass('btn-primary').addClass('btn-info');
        $.ajax({
            type: "POST",
            // define url name
            url: "{% url 'doxer_admin:allpassenger' %}", 
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

                        if(val.status == 'Active'){
                            //var status = "<input type='checkbox' class='check-blocks' data-sid='" +val.id+ "'>&nbsp;<label class='badge badge-success'>Active</label>";
                            var status = "<div class='onoffswitch'><input type='checkbox' name='onoffswitch' data-sid='" +val.id+ "' class='check-block onoffswitch-checkbox' id='myonoffswitch"+val.id+"' checked><label class='onoffswitch-label' for='myonoffswitch"+val.id+"'><div class='onoffswitch-inner'></div><div class='onoffswitch-switch'></div></label></div>";
                        } else if(val.status == 'Deactive'){
                            var status = "<div class='onoffswitch'><input type='checkbox' name='onoffswitch' data-sid='" +val.id+ "' class='check-block onoffswitch-checkbox' id='myonoffswitch"+val.id+"'><label class='onoffswitch-label' for='myonoffswitch"+val.id+"'><div class='onoffswitch-inner'></div><div class='onoffswitch-switch'></div></label></div>";
                        } else {
                            var status = '';
                        }
    
                        if(val.id_status == 'P'){
                            var buttons = "<div class='nav-item dropdown language-dropdown d-none d-sm-flex align-items-center btn-approval' dataid='"+ val.id +"' sta='"+ val.id_status +"'><a class='nav-link d-flex align-items-center dropdown-toggle btn btn-info' id='LanguageDropdown' href='javascript:void(0);' data-toggle='dropdown' aria-expanded='false'><span class='profile-text font-weight-normal' id='mains'>Pending</span></a><div class='dropdown-menu dropdown-menu-left navbar-dropdown py-2 ' aria-labelledby='LanguageDropdown'><a class='dropdown-item active' dataid='"+ val.id +"' datast='P'> Pending </a><a class='dropdown-item' dataid='"+ val.id +"' datast='A'> Approve </a><a class='dropdown-item' dataid='"+ val.id +"' datast='R'> Reject </a></div></div> ";
                        }
                        if(val.id_status == 'A'){
                            var buttons = "<div class='nav-item dropdown language-dropdown d-none d-sm-flex align-items-center btn-approval' dataid='"+ val.id +"' sta='"+ val.id_status +"'><a class='nav-link d-flex align-items-center dropdown-toggle btn btn-success' id='LanguageDropdown' href='javascript:void(0);' data-toggle='dropdown' aria-expanded='false'><span class='profile-text font-weight-normal' id='mains'>Approved</span></a><div class='dropdown-menu dropdown-menu-left navbar-dropdown py-2 ' aria-labelledby='LanguageDropdown'><a class='dropdown-item' dataid='"+ val.id +"' datast='P'> Pending </a><a class='dropdown-item active' dataid='"+ val.id +"' datast='A'> Approve </a><a class='dropdown-item' dataid='"+ val.id +"' datast='R'> Reject </a></div></div> ";
                        }
                        if(val.id_status == 'R'){
                            var buttons = "<div class='nav-item dropdown language-dropdown d-none d-sm-flex align-items-center btn-approval' dataid='"+ val.id +"' sta='"+ val.id_status +"'><a class='nav-link d-flex align-items-center dropdown-toggle btn btn-danger' id='LanguageDropdown' href='javascript:void(0);' data-toggle='dropdown' aria-expanded='false'><span class='profile-text font-weight-normal' id='mains'>Rejected</span></a><div class='dropdown-menu dropdown-menu-left navbar-dropdown py-2 ' aria-labelledby='LanguageDropdown'><a class='dropdown-item' dataid='"+ val.id +"' datast='P'> Pending </a><a class='dropdown-item' dataid='"+ val.id +"' datast='A'> Approve </a><a class='dropdown-item active' dataid='"+ val.id +"' datast='R'> Reject </a></div></div> ";
                        }
    
                        // $('#tests-table').append("<tr><td> # " + val.id  + "</td><td>" + "<img src=" +val.pro_image + " alt='profile' /><span class='pl-2'>" + val.username + "</span></td><td>"+ val.email +"</td><td>"+ val.contact_no +"</td><td>" + val.gender + "</td><td id='"+val.id+"'>"+ status + "</td><td>" +val.id_proofe+ "</td><td id='btn"+val.id+"'>" + buttons + "</td><td>"+ val.create_at +"</td></tr>")
                        $('#tests-table').append("<tr><td> # " + val.id  + "</td><td>" + "<img src=" +val.pro_image + " alt='profile' /><span class='pl-2'>" + val.username + "</span></td><td>"+ val.email +"</td><td>"+ val.contact_no +"</td><td>" + val.gender + "</td><td id='"+val.id+"'>"+ status + "</td><td>" +val.id_proofe+ "</td><td>"+ val.create_at +"</td></tr>")
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
        $('#tests-table').html('');
        $('#tests-table').append("<tr><th colspan=9><center><div class='spinner-border' role='status'></div></center></th></tr>");
        var currentpage = $('.pagination li.active').index();
        var nextpage = currentpage + 1;
        $.ajax({
            type: "POST",
            // define url name
            url: "{% url 'doxer_admin:allpassenger' %}", 
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
                        if(val.status == 'Active'){
                            //var status = "<input type='checkbox' class='check-blocks' data-sid='" +val.id+ "'>&nbsp;<label class='badge badge-success'>Active</label>";
                            var status = "<div class='onoffswitch'><input type='checkbox' name='onoffswitch' data-sid='" +val.id+ "' class='check-block onoffswitch-checkbox' id='myonoffswitch"+val.id+"' checked><label class='onoffswitch-label' for='myonoffswitch"+val.id+"'><div class='onoffswitch-inner'></div><div class='onoffswitch-switch'></div></label></div>";
                        } else if(val.status == 'Deactive'){
                            var status = "<div class='onoffswitch'><input type='checkbox' name='onoffswitch' data-sid='" +val.id+ "' class='check-block onoffswitch-checkbox' id='myonoffswitch"+val.id+"'><label class='onoffswitch-label' for='myonoffswitch"+val.id+"'><div class='onoffswitch-inner'></div><div class='onoffswitch-switch'></div></label></div>";
                        } else {
                            var status = '';
                        }
    
                        if(val.id_status == 'P'){
                            var buttons = "<div class='nav-item dropdown language-dropdown d-none d-sm-flex align-items-center btn-approval' dataid='"+ val.id +"' sta='"+ val.id_status +"'><a class='nav-link d-flex align-items-center dropdown-toggle btn btn-info' id='LanguageDropdown' href='javascript:void(0);' data-toggle='dropdown' aria-expanded='false'><span class='profile-text font-weight-normal' id='mains'>Pending</span></a><div class='dropdown-menu dropdown-menu-left navbar-dropdown py-2 ' aria-labelledby='LanguageDropdown'><a class='dropdown-item active' dataid='"+ val.id +"' datast='P'> Pending </a><a class='dropdown-item' dataid='"+ val.id +"' datast='A'> Approve </a><a class='dropdown-item' dataid='"+ val.id +"' datast='R'> Reject </a></div></div> ";
                        }
                        if(val.id_status == 'A'){
                            var buttons = "<div class='nav-item dropdown language-dropdown d-none d-sm-flex align-items-center btn-approval' dataid='"+ val.id +"' sta='"+ val.id_status +"'><a class='nav-link d-flex align-items-center dropdown-toggle btn btn-success' id='LanguageDropdown' href='javascript:void(0);' data-toggle='dropdown' aria-expanded='false'><span class='profile-text font-weight-normal' id='mains'>Approved</span></a><div class='dropdown-menu dropdown-menu-left navbar-dropdown py-2 ' aria-labelledby='LanguageDropdown'><a class='dropdown-item' dataid='"+ val.id +"' datast='P'> Pending </a><a class='dropdown-item active' dataid='"+ val.id +"' datast='A'> Approve </a><a class='dropdown-item' dataid='"+ val.id +"' datast='R'> Reject </a></div></div> ";
                        }
                        if(val.id_status == 'R'){
                            var buttons = "<div class='nav-item dropdown language-dropdown d-none d-sm-flex align-items-center btn-approval' dataid='"+ val.id +"' sta='"+ val.id_status +"'><a class='nav-link d-flex align-items-center dropdown-toggle btn btn-danger' id='LanguageDropdown' href='javascript:void(0);' data-toggle='dropdown' aria-expanded='false'><span class='profile-text font-weight-normal' id='mains'>Rejected</span></a><div class='dropdown-menu dropdown-menu-left navbar-dropdown py-2 ' aria-labelledby='LanguageDropdown'><a class='dropdown-item' dataid='"+ val.id +"' datast='P'> Pending </a><a class='dropdown-item' dataid='"+ val.id +"' datast='A'> Approve </a><a class='dropdown-item active' dataid='"+ val.id +"' datast='R'> Reject </a></div></div> ";
                        }
    
                        // $('#tests-table').append("<tr><td> # " + val.id  + "</td><td>" + "<img src=" +val.pro_image + " alt='profile' /><span class='pl-2'>" + val.username + "</span></td><td>"+ val.email +"</td><td>"+ val.contact_no +"</td><td>" + val.gender + "</td><td id='"+val.id+"'>"+ status + "</td><td>" +val.id_proofe+ "</td><td id='btn"+val.id+"'>" + buttons + "</td><td>"+ val.create_at +"</td></tr>")
                        $('#tests-table').append("<tr><td> # " + val.id  + "</td><td>" + "<img src=" +val.pro_image + " alt='profile' /><span class='pl-2'>" + val.username + "</span></td><td>"+ val.email +"</td><td>"+ val.contact_no +"</td><td>" + val.gender + "</td><td id='"+val.id+"'>"+ status + "</td><td>" +val.id_proofe+ "</td><td>"+ val.create_at +"</td></tr>")
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
        $('#tests-table').append("<tr><th colspan=9><center><div class='spinner-border' role='status'></div></center></th></tr>");
        $("#prev-page").removeAttr('disabled');
        $("#next-page").removeAttr('disabled');
        var currentpage = $('.pagination li.active').index();
        var nextpage = currentpage - 1;
        $.ajax({
            type: "POST",
            // define url name
            url: "{% url 'doxer_admin:allpassenger' %}", 
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
                        if(val.status == 'Active'){
                            //var status = "<input type='checkbox' class='check-blocks' data-sid='" +val.id+ "'>&nbsp;<label class='badge badge-success'>Active</label>";
                            var status = "<div class='onoffswitch'><input type='checkbox' name='onoffswitch' data-sid='" +val.id+ "' class='check-block onoffswitch-checkbox' id='myonoffswitch"+val.id+"' checked><label class='onoffswitch-label' for='myonoffswitch"+val.id+"'><div class='onoffswitch-inner'></div><div class='onoffswitch-switch'></div></label></div>";
                        } else if(val.status == 'Deactive'){
                            var status = "<div class='onoffswitch'><input type='checkbox' name='onoffswitch' data-sid='" +val.id+ "' class='check-block onoffswitch-checkbox' id='myonoffswitch"+val.id+"'><label class='onoffswitch-label' for='myonoffswitch"+val.id+"'><div class='onoffswitch-inner'></div><div class='onoffswitch-switch'></div></label></div>";
                        } else {
                            var status = '';
                        }
    
                        if(val.id_status == 'P'){
                            var buttons = "<div class='nav-item dropdown language-dropdown d-none d-sm-flex align-items-center btn-approval' dataid='"+ val.id +"' sta='"+ val.id_status +"'><a class='nav-link d-flex align-items-center dropdown-toggle btn btn-info' id='LanguageDropdown' href='javascript:void(0);' data-toggle='dropdown' aria-expanded='false'><span class='profile-text font-weight-normal' id='mains'>Pending</span></a><div class='dropdown-menu dropdown-menu-left navbar-dropdown py-2 ' aria-labelledby='LanguageDropdown'><a class='dropdown-item active' dataid='"+ val.id +"' datast='P'> Pending </a><a class='dropdown-item' dataid='"+ val.id +"' datast='A'> Approve </a><a class='dropdown-item' dataid='"+ val.id +"' datast='R'> Reject </a></div></div> ";
                        }
                        if(val.id_status == 'A'){
                            var buttons = "<div class='nav-item dropdown language-dropdown d-none d-sm-flex align-items-center btn-approval' dataid='"+ val.id +"' sta='"+ val.id_status +"'><a class='nav-link d-flex align-items-center dropdown-toggle btn btn-success' id='LanguageDropdown' href='javascript:void(0);' data-toggle='dropdown' aria-expanded='false'><span class='profile-text font-weight-normal' id='mains'>Approved</span></a><div class='dropdown-menu dropdown-menu-left navbar-dropdown py-2 ' aria-labelledby='LanguageDropdown'><a class='dropdown-item' dataid='"+ val.id +"' datast='P'> Pending </a><a class='dropdown-item active' dataid='"+ val.id +"' datast='A'> Approve </a><a class='dropdown-item' dataid='"+ val.id +"' datast='R'> Reject </a></div></div> ";
                        }
                        if(val.id_status == 'R'){
                            var buttons = "<div class='nav-item dropdown language-dropdown d-none d-sm-flex align-items-center btn-approval' dataid='"+ val.id +"' sta='"+ val.id_status +"'><a class='nav-link d-flex align-items-center dropdown-toggle btn btn-danger' id='LanguageDropdown' href='javascript:void(0);' data-toggle='dropdown' aria-expanded='false'><span class='profile-text font-weight-normal' id='mains'>Rejected</span></a><div class='dropdown-menu dropdown-menu-left navbar-dropdown py-2 ' aria-labelledby='LanguageDropdown'><a class='dropdown-item' dataid='"+ val.id +"' datast='P'> Pending </a><a class='dropdown-item' dataid='"+ val.id +"' datast='A'> Approve </a><a class='dropdown-item active' dataid='"+ val.id +"' datast='R'> Reject </a></div></div> ";
                        }
    
                        // $('#tests-table').append("<tr><td> # " + val.id  + "</td><td>" + "<img src=" +val.pro_image + " alt='profile' /><span class='pl-2'>" + val.username + "</span></td><td>"+ val.email +"</td><td>"+ val.contact_no +"</td><td>" + val.gender + "</td><td id='"+val.id+"'>"+ status + "</td><td>" +val.id_proofe+ "</td><td id='btn"+val.id+"'>" + buttons + "</td><td>"+ val.create_at +"</td></tr>")
                        $('#tests-table').append("<tr><td> # " + val.id  + "</td><td>" + "<img src=" +val.pro_image + " alt='profile' /><span class='pl-2'>" + val.username + "</span></td><td>"+ val.email +"</td><td>"+ val.contact_no +"</td><td>" + val.gender + "</td><td id='"+val.id+"'>"+ status + "</td><td>" +val.id_proofe+ "</td><td>"+ val.create_at +"</td></tr>")
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
    $('#tests-table').append("<tr><th colspan=9><center><div class='spinner-border' role='status'></div></center></th></tr>");
    $.ajax({
        type: "POST",
        url: "{% url 'doxer_admin:allpassenger' %}", 
        data : {'page_no' : page_no, csrfmiddlewaretoken: '{{ csrf_token }}'},
        // handle a successful response
        success: function (data) {
            $("#et1").text(data.a);
            $("#et2").text(data.b);
            $("#totale").text(data.t);
            if (data.results == ''){
                $('#tests-table').html('');
                $('#tests-table').append("<tr><th colspan=9><center>No Records</center></th></tr>");
            } else {
                $('#tests-table').html('');
                $('.pagination ').fadeIn();
                $.each(data.results, function(i, val) {
                    //append to post
                    for(var j=1 ; j <= i ; j++){j};
                    if(val.status == 'Active'){
                        //var status = "<input type='checkbox' class='check-blocks' data-sid='" +val.id+ "'>&nbsp;<label class='badge badge-success'>Active</label>";
                        var status = "<div class='onoffswitch'><input type='checkbox' name='onoffswitch' data-sid='" +val.id+ "' class='check-block onoffswitch-checkbox' id='myonoffswitch"+val.id+"' checked><label class='onoffswitch-label' for='myonoffswitch"+val.id+"'><div class='onoffswitch-inner'></div><div class='onoffswitch-switch'></div></label></div>";
                    } else if(val.status == 'Deactive'){
                        var status = "<div class='onoffswitch'><input type='checkbox' name='onoffswitch' data-sid='" +val.id+ "' class='check-block onoffswitch-checkbox' id='myonoffswitch"+val.id+"'><label class='onoffswitch-label' for='myonoffswitch"+val.id+"'><div class='onoffswitch-inner'></div><div class='onoffswitch-switch'></div></label></div>";
                    } else {
                        var status = '';
                    }

                    if(val.id_status == 'P'){
                        var buttons = "<div class='nav-item dropdown language-dropdown d-none d-sm-flex align-items-center btn-approval' dataid='"+ val.id +"' sta='"+ val.id_status +"'><a class='nav-link d-flex align-items-center dropdown-toggle btn btn-info' id='LanguageDropdown' href='javascript:void(0);' data-toggle='dropdown' aria-expanded='false'><span class='profile-text font-weight-normal' id='mains'>Pending</span></a><div class='dropdown-menu dropdown-menu-left navbar-dropdown py-2 ' aria-labelledby='LanguageDropdown'><a class='dropdown-item active' dataid='"+ val.id +"' datast='P'> Pending </a><a class='dropdown-item' dataid='"+ val.id +"' datast='A'> Approve </a><a class='dropdown-item' dataid='"+ val.id +"' datast='R'> Reject </a></div></div> ";
                    }
                    if(val.id_status == 'A'){
                        var buttons = "<div class='nav-item dropdown language-dropdown d-none d-sm-flex align-items-center btn-approval' dataid='"+ val.id +"' sta='"+ val.id_status +"'><a class='nav-link d-flex align-items-center dropdown-toggle btn btn-success' id='LanguageDropdown' href='javascript:void(0);' data-toggle='dropdown' aria-expanded='false'><span class='profile-text font-weight-normal' id='mains'>Approved</span></a><div class='dropdown-menu dropdown-menu-left navbar-dropdown py-2 ' aria-labelledby='LanguageDropdown'><a class='dropdown-item' dataid='"+ val.id +"' datast='P'> Pending </a><a class='dropdown-item active' dataid='"+ val.id +"' datast='A'> Approve </a><a class='dropdown-item' dataid='"+ val.id +"' datast='R'> Reject </a></div></div> ";
                    }
                    if(val.id_status == 'R'){
                        var buttons = "<div class='nav-item dropdown language-dropdown d-none d-sm-flex align-items-center btn-approval' dataid='"+ val.id +"' sta='"+ val.id_status +"'><a class='nav-link d-flex align-items-center dropdown-toggle btn btn-danger' id='LanguageDropdown' href='javascript:void(0);' data-toggle='dropdown' aria-expanded='false'><span class='profile-text font-weight-normal' id='mains'>Rejected</span></a><div class='dropdown-menu dropdown-menu-left navbar-dropdown py-2 ' aria-labelledby='LanguageDropdown'><a class='dropdown-item' dataid='"+ val.id +"' datast='P'> Pending </a><a class='dropdown-item' dataid='"+ val.id +"' datast='A'> Approve </a><a class='dropdown-item active' dataid='"+ val.id +"' datast='R'> Reject </a></div></div> ";
                    }

                    $('#tests-table').append("<tr><td> # " + val.id  + "</td><td>" + "<img src=" +val.pro_image + " alt='profile' /><span class='pl-2'>" + val.username + "</span></td><td>"+ val.email +"</td><td>"+ val.contact_no +"</td><td>" + val.gender + "</td><td id='"+val.id+"'>"+ status + "</td><td>" +val.id_proofe+ "</td><td>"+ val.create_at +"</td></tr>")
                    // $('#tests-table').append("<tr><td> # " + val.id  + "</td><td>" + "<img src=" +val.pro_image + " alt='profile' /><span class='pl-2'>" + val.username + "</span></td><td>"+ val.email +"</td><td>"+ val.contact_no +"</td><td>" + val.gender + "</td><td id='"+val.id+"'>"+ status + "</td><td>" +val.id_proofe+ "</td><td id='btn"+val.id+"'>" + buttons + "</td><td>"+ val.create_at +"</td></tr>")
                    });
                }
            },
            error: function () {
                alert('Page Not Founded');
            }
    }); 
});

$('tbody').on('click','.documentview',function(){
    var id = $(this).attr('data');
    $.ajax({
        type : "POST",
        url: "{% url 'doxer_admin:showid' pk='2' %}", 
        data : {'id' : id, csrfmiddlewaretoken: '{{ csrf_token }}'},
        success: function (data) {
            $('#IdProofe').html('');
            $('#IdProofename').text(data.name);
            if(data.id2 == '0'){
                $('#IdProofe').append("<div class='' id='IdProofe1'><img src='"+ data.id1 +"' alt='IdProofe1'></div>");
            } else {
                $('#IdProofe').append("<div class='col-md-6' id='IdProofe1'><img src='"+ data.id1 +"' alt='IdProofe1'></div><div class='col-md-6' id='IdProofe2'><img src='"+ data.id2 +"' alt='IdProofe2'></div>");
            }
        },
        error: function () {
            alert('Page Not Founded');
        }
    });
});


$(document).ready(function () {   
    $('tbody').on('click','.btn-approval',function(){
        $('.dropdown-menu a').on('click',function(){
            var sid = $(this).attr('dataid');
            var get_status = $(this).attr('datast');
            var text = $(this).text();

            $.ajax({
                type : "POST",
                url: "{% url 'doxer_admin:Id_Approval' pk='2' %}", 
                data : {'id' : sid, 'sta' : get_status, csrfmiddlewaretoken: '{{ csrf_token }}'},
                success: function (data) {
                    if(data.status == 1 && data.st == 'A'){
                        $('#btn'+data.getid).html('');
                        $('#btn'+data.getid).append("<div class='nav-item dropdown language-dropdown d-none d-sm-flex align-items-center btn-approval' dataid='"+ sid +"' sta='"+ data.st +"'><a class='nav-link d-flex align-items-center dropdown-toggle btn btn-success' id='LanguageDropdown' href='javascript:void(0);' data-toggle='dropdown' aria-expanded='false'><span class='profile-text font-weight-normal' id='mains'> "+ data.msg +" </span></a><div class='dropdown-menu dropdown-menu-left navbar-dropdown py-2 ' aria-labelledby='LanguageDropdown'><a class='dropdown-item' dataid='"+ data.getid +"' datast='P'> Pending </a><a class='dropdown-item active' dataid='"+ data.getid +"' datast='A'> Approve </a><a class='dropdown-item' dataid='"+ data.getid +"' datast='R'> Reject </a></div></div>");
                    } else if(data.status == 1 && data.st == 'R'){
                        $('#btn'+data.getid).html('');
                        $('#btn'+data.getid).append("<div class='nav-item dropdown language-dropdown d-none d-sm-flex align-items-center btn-approval' dataid='"+ sid +"' sta='"+ data.st +"'><a class='nav-link d-flex align-items-center dropdown-toggle btn btn-danger' id='LanguageDropdown' href='javascript:void(0);' data-toggle='dropdown' aria-expanded='false'><span class='profile-text font-weight-normal' id='mains'> "+ data.msg +" </span></a><div class='dropdown-menu dropdown-menu-left navbar-dropdown py-2 ' aria-labelledby='LanguageDropdown'><a class='dropdown-item' dataid='"+ data.getid +"' datast='P'> Pending </a><a class='dropdown-item' dataid='"+ data.getid +"' datast='A'> Approve </a><a class='dropdown-item active' dataid='"+ data.getid +"' datast='R'> Reject </a></div></div>");
                    }
                    else if(data.status == 1 && data.st == 'P'){
                        $('#btn'+data.getid).html('');
                        $('#btn'+data.getid).append("<div class='nav-item dropdown language-dropdown d-none d-sm-flex align-items-center btn-approval' dataid='"+ sid +"' sta='"+ data.st +"'><a class='nav-link d-flex align-items-center dropdown-toggle btn btn-info' id='LanguageDropdown' href='javascript:void(0);' data-toggle='dropdown' aria-expanded='false'><span class='profile-text font-weight-normal' id='mains'> "+ data.msg +" </span></a><div class='dropdown-menu dropdown-menu-left navbar-dropdown py-2 ' aria-labelledby='LanguageDropdown'><a class='dropdown-item active' dataid='"+ data.getid +"' datast='P'> Pending </a><a class='dropdown-item' dataid='"+ data.getid +"' datast='A'> Approve </a><a class='dropdown-item' dataid='"+ data.getid +"' datast='R'> Reject </a></div></div>");
                    } else {
                        $('#btn'+data.getid).html('');
                    }
                    if(data.status == 0){
                    }
                },
                error: function () {
                    alert('Page Not Founded');
                }
        });
        });
    });
});
