
function initMap() {

    const locations = JSON.parse(document.getElementById('locations').getAttribute("locations"))
    var directionsService = new google.maps.DirectionsService();
    var directionsRenderer = new google.maps.DirectionsRenderer();
    // convert locations[list of list] to list of dict
    const laglngs = []

    locations.map((position, i) => {
        laglngs.push({ lat: position[0], lng: position[1] })
    });

    // const location_names = JSON.parse(document.getElementById('location_names').getAttribute("location_names"));


    const startLatLng = laglngs[0];

    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 11,
        center: startLatLng,
        gestureHandling: "greedy",
        mapId:'d5a1921b1f1eed54'
    });


    //const svgMarker = {
    //    path: "M-1.547 12l6.563-6.609-1.406-1.406-5.156 5.203-2.063-2.109-1.406 1.406zM0 0q2.906 0 4.945 2.039t2.039 4.945q0 1.453-0.727 3.328t-1.758 3.516-2.039 3.070-1.711 2.273l-0.75 0.797q-0.281-0.328-0.75-0.867t-1.688-2.156-2.133-3.141-1.664-3.445-0.75-3.375q0-2.906 2.039-4.945t4.945-2.039z",
    //    fillColor: "#00468b",
    //    fillOpacity: 1,
    //    strokeWeight: 0,
    //    rotation: 0,
    //    scale: 2,
    //    anchor: new google.maps.Point(0, 20),
    //};

    //laglngs.map((laglng, i) => {
    //    let num = i
    //    new google.maps.Marker({
    //        position: laglng,
    //        map: map,
    //        icon: svgMarker,
    //        //label: num.toString(),
    //        animation: google.maps.Animation.DROP,
    //        // title: location_names[i].replaceAll("_"," "),
    //    })

    //});



    directionsRenderer.setMap(map)
    calcRoute(directionsService, directionsRenderer, locations)
    }
    function calcRoute(directionsService, directionsRenderer, locations) {
      const waypts = [];

      for (let i = 1; i < locations.length-1; i++) {
          waypts.push({
            location: new google.maps.LatLng(locations[i][0], locations[i][1]),
            stopover: true,
          });
      }
      directionsService
        .route({
          origin: new google.maps.LatLng(locations[0][0], locations[0][1]),
          destination: new google.maps.LatLng(locations[locations.length-1][0], locations[locations.length-1][1]),
          waypoints: waypts,
          optimizeWaypoints: true,
          travelMode: google.maps.TravelMode.WALKING,
        })
        .then((response) => {
          directionsRenderer.setDirections(response);
    })
}

window.initMap = initMap;

