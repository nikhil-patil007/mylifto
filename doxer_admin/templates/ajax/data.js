$('tbody').on('click','.check-blocks',function(){
    var id = $(this).attr('data-sid');
    mydata = {pid:id, 'csrfmiddlewaretoken': '{{ csrf_token }}'}
    mythis = this;
    $.ajax({
        url : "{% url 'doxer_admin:blockdri' %}",
        method : "POST",
        data : mydata,
        success : function(data){
            if (data.status==1){
                $('#'+id).html('');
                // $('#errormsg').append("<div class='alert alert-danger' id='pass"+id+"'>"+ data.driver +"</div>")
                $('#'+id).append("<div class='onoffswitch'><input type='checkbox' name='onoffswitch' data-sid='" +id+ "' class='check-blocks onoffswitch-checkbox' id='myonoffswitch"+id+"'><label class='onoffswitch-label' for='myonoffswitch"+id+"'><div class='onoffswitch-inner'></div><div class='onoffswitch-switch'></div></label></div>");
            }
            if (data.status==2){
                $('#'+id).html('');
                // $('#errormsg').append("<div class='alert alert-success' id='pass"+id+"'>"+ data.driver +"</div>")
                $('#'+id).append("<div class='onoffswitch'><input type='checkbox' name='onoffswitch' data-sid='" +id+ "' class='check-blocks onoffswitch-checkbox' id='myonoffswitch"+id+"' checked><label class='onoffswitch-label' for='myonoffswitch"+id+"'><div class='onoffswitch-inner'></div><div class='onoffswitch-switch'></div></label></div>"); 
            }
            if (data.status==0){
                // console.log("Unable To Delete User")
            }
        },
    });
});

$('tbody').on('click','.edit-btn',function(){
    let id = $(this).attr('data-sid');
    mydata = {pid:id, 'csrfmiddlewaretoken': '{{ csrf_token }}'}
    mythis = this;
    // console.log(mythis)
    $.ajax({
        url : "{% url 'doxer_admin:editprices' %}",
        method : "POST",
        data : mydata,
        dataType : "json",
        success : function(data){
            if (data.status==0){
                console.log('status 0')
                setTimeout(function() {
                    $('#modelsget').modal('hide');
                }, 800);
            } else {
                // console.log(data);
                $('#myModalLabel').text(data.email);
                $("#price").val(data.fees);
                $("#saveprice").attr('data-sid',data.id);
            }
        },
    });
});

// Update Page Fare Per Km
$(".saveprice").on('click',function(){
    var id = $(this).attr('data-sid');
    let price = $('#price').val();
    $(".saveprice").text("Please Wait...."); 
    $('.saveprice').attr('disabled', 'disabled');
    mydata = {'pid':id, 'csrfmiddlewaretoken': '{{ csrf_token }}','price' : price}
        $.ajax({
        url : "{% url 'doxer_admin:updatepriceb' %}",
        method : "POST",
        data : mydata,
        success : function(data){
            if (data.status==1){
                setTimeout(function() {
                    $('#modelsget').modal('hide');
                }, 1000);
                setTimeout(function() {
                    $('.saveprice').removeAttr('disabled');
                    $(".saveprice").text("Update");
                    $('#pr'+id).html('');
                    $('#pr'+id).append("₹ "+price +"")
                }, 2000);
            }
            if (data.status==2){
                $('label#name_label').removeAttr('hidden');
                $('.saveprice').removeAttr('disabled');
                $(".saveprice").text("Update");
    
            }
            if (data.status==0){
                console.log("Unable To Update Price")
            }
        },
    });
});

$('tbody').on('click','.documentview',function(){
    var id = $(this).attr('data');
    $.ajax({
        type : "POST",
        url: "{% url 'doxer_admin:showid' pk='1' %}", 
        data : {'id' : id, csrfmiddlewaretoken: '{{ csrf_token }}'},
        success: function (data) {
            $('#IdProofe1').html('');
            $('#IdProofe2').html('');
            $('#IdProofename').text(data.name);
            $('#IdProofe1').append("<img src="+ data.id1 +" alt='IdProofe1'>");
            $('#IdProofe2').append("<img src="+ data.id2 +" alt='IdProofe2'>");
        },
        error: function () {
            alert('Page Not Founded');
        }
    });
});