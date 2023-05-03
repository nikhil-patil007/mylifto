{% load static %}
$.getScript("https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places")
    .done(function(script, textStatus) {
        google.maps.event.addDomListener(window, "load", initMap)

    })
    function initMap() {
        var directionsService = new google.maps.DirectionsService;
        var directionsDisplay = new google.maps.DirectionsRenderer;
        if (status == "P"){
            var map = new google.maps.Map(document.getElementById('map-route'), {
                zoom: 9,
                maxZoom: 16,
                center: { lat: lat_a, lng: long_a }
            });
        }
        if (status == 'O'){
            var map = new google.maps.Map(document.getElementById('map-route'), {
                // zoom: 6,
                // maxZoom: 16,
                // minZoom: 8,
                // center: { lat: lat_a, lng: long_a },
                //mapTypeId: "hybrid",
            });
            setInterval(function(){
                var currentposition = $("#map-route").attr('currentposition');
                var currentposition2 = $("#map-route").attr('currentposition2');
                var status = $("#map-route").attr('status');
                var lat = currentposition;
                if(status == 'E'){
                    location.reload();
                } else {
                    console.log('------------status-------',status);
                }
                    if(car == 'C'){
                        var marker = new google.maps.Marker({
                            position: new google.maps.LatLng(currentposition,currentposition2),
                            draggable: true,
                            icon : "{% static 'images/Doxer_car_image1.png' %}",
                            // icon : "{% static 'images/car.png' %}",
                            // animation: google.maps.Animation.DROP,
                            // icon: {
                            //       path: google.maps.SymbolPath.CIRCLE,
                            //       scale: 10,
                            //       strokeColor: "#393",
                            //       
                            // },
                            draggable: true,
                        });
                    } else {
                        var marker = new google.maps.Marker({
                            position: new google.maps.LatLng(currentposition,currentposition2),
                            draggable: true,
                            icon : "{% static 'images/Truck.png' %}",
                            draggable: true,
                        });
                    }
                    setTimeout(function(){
                        marker.setMap(null);
                    },1000);
                    marker.setMap(map);
                },1000);
        }
        if(status == 'E'){
            console.log('end Trip all');
            var currentposition = parseFloat($("#map-route").attr('currentposition'));
            var currentposition2 = parseFloat($("#map-route").attr('currentposition2'));
            var map = new google.maps.Map(document.getElementById('map-route'), {
            zoom: 7,
            maxZoom: 16,
            minZoom: 8,
            center: { lat: currentposition, lng: currentposition2 }
        });
            var currentposition = $("#map-route").attr('currentposition');
            var currentposition2 = $("#map-route").attr('currentposition2');
            var lat = currentposition;
                var marker = new google.maps.Marker({
                    title : "Driver's Locations",
                    position: new google.maps.LatLng(currentposition,currentposition2),
                    // icon : "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
                    
                });
                marker.setMap(map);
        }
            directionsDisplay.setMap(map);
        calculateAndDisplayRoute(directionsService, directionsDisplay);
        
    }


function calculateAndDisplayRoute(directionsService, directionsDisplay) {
    if(status == 'O'){
        var currentposition = $("#map-route").attr('currentposition');
        var currentposition2 = $("#map-route").attr('currentposition2');
        var origin2 = currentposition+','+currentposition2;
        console.log('end Trip',origin2);
        directionsService.route({
            origin: origin2,
            destination: destination,
            travelMode: 'DRIVING'
        }, function(response, status) {
            if (status === 'OK') {
                directionsDisplay.setDirections(response);
            } else {
                alert('Directions request failed due to ' + status);
                url = "{% url 'doxer_admin:allrides' %}"
                window.location.assign(url)
            }
        });
    } else {
        directionsService.route({
            origin: origin,
            destination: destination,
            travelMode: 'DRIVING'
            // travelMode: 'TRANSIT'
        }, function(response, status) {
            if (status === 'OK') {
                directionsDisplay.setDirections(response);
            } else {
                alert('Directions request failed due to ' + status);
                url = "{% url 'doxer_admin:allrides' %}"
                window.location.assign(url)
            }
        });
    }
}