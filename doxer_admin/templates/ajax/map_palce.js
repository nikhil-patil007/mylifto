var google_api_key = "{{google_api_key|safe}}";

$(document).on('click','#pleaseclickme',function(){
    $.getScript("https://maps.googleapis.com/maps/api/js?key={{google_api_key}}&libraries=places")
    .done(function(script, textStatus) {
        google.maps.event.addDomListener(window,'load',CalcRoute())
    })
    setTimeout(function(){
        $("#id-lat-a").val('');
        $("#id-long-a").val('');
        $("#id-lat-b").val('');
        $("#id-long-b").val('');
        $("#id-rid-a").val('');
    },1000);
});

  function validateForm() {
      var valid = true;
      $('.geo').each(function() {
          if ($(this).val() === '') {
              valid = false;
              return false;
          }
      });
      return valid
  }

function CalcRoute() {
    if (validateForm() == true) {
        var params = {
            lat_a: $('#id-lat-a').val(),
            long_a: $('#id-long-a').val(),
            lat_b: $('#id-lat-b').val(),
            long_b: $('#id-long-b').val(),
            rid: $('#id-rid-a').val(),
        };
        var mapid = $('#id-rid-link').val();
        var esc = encodeURIComponent;
        var query = Object.keys(params)
        .map(k => esc(k) + '=' + esc(params[k]))
        .join('&');

        url = mapid + '?' + query
        window.location.assign(url)
    }
    
}