function initMap() {
    const myLatLng = { lat: 44.350011499069, lng: -68.2414535993951 };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 11,
        center: myLatLng,
        gestureHandling: "greedy"
    });
    const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    //new google.maps.Marker({
    //    position: myLatLng,
    //    map,
    //    label: "A"
    //});

    //new google.maps.Marker({
    //    position: { lat: 44.3300018310546, lng: -68.1775283813476 },
    //    map,
    //    label: "B"
    //});

    const locations = [
        { lat: 44.350011499069, lng: -68.2414535993951 },
        { lat: 44.3300018310546, lng: -68.1775283813476 },
        { lat: 44.2284927368164, lng: -68.3237609863281 },
        { lat: 44.35079167, lng: -68.30218833 },
        { lat: 44.372621, lng: -68.221942 },
        { lat: 44.23383331298821, lng: -68.3199996948242 },
        { lat: 44.3585023529493, lng: -68.2059851525353 },
  
    ];

    locations.map((position, i) => {
        
        const label = labels[i % labels.length];
        console.log(label)
        new google.maps.Marker({
            position: position,
            map,
            label: label,
        })

    });

    const flightPlanCoordinates = [
        { lat: 44.350011499069, lng: -68.2414535993951 },
        { lat: 44.3300018310546, lng: -68.1775283813476 },
        { lat: 44.2284927368164, lng: -68.3237609863281 },
        { lat: 44.35079167, lng: -68.30218833 },
        { lat: 44.372621, lng: -68.221942 },
        { lat: 44.23383331298821, lng: -68.3199996948242 },
        { lat: 44.3585023529493, lng: -68.2059851525353 },

    ];
    const flightPath = new google.maps.Polyline({
        path: flightPlanCoordinates,
        geodesic: true,
        strokeColor: "#0000FF",
        strokeOpacity: 1.0,
        strokeWeight: 2,
    });

    flightPath.setMap(map);


}



window.initMap = initMap;
