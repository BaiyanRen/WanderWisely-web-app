
//var locations;

//function setLocations(locations) {
//    console.log("aaaa")
//    //this.locations = locations;


//}



function initMap() {
  var directionsService = new google.maps.DirectionsService();
  var directionsRenderer = new google.maps.DirectionsRenderer();
    const myLatLng = { lat: 44.350011499069, lng: -68.2414535993951 };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 11,
        center: myLatLng,
        gestureHandling: "greedy"
    });
    const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";


    // const locations = [
    //    { lat: 44.372621, lng: -68.221942 },
    //    { lat: 44.35079167, lng: -68.30218833 },
    //    { lat: 44.23383331298821, lng: -68.3199996948242 },
    //    { lat: 44.2284927368164, lng: -68.3237609863281 },
    //    { lat: 44.350011499069, lng: -68.2414535993951 },
    //    { lat: 44.3585023529493, lng: -68.2059851525353 },
    //    { lat: 44.3300018310546, lng: -68.1775283813476 },

    // ];

    //console.log("aaaaaaaaaaaaa")
    const locations = JSON.parse(document.getElementById('locations').getAttribute("locations"))
    //console.log(locations)
    // const objectRegex = /(\{(.*?)(\}('|")\}))/g;

    // const object = data.match(objectRegex).map(match => JSON.parse(match.replace(/'(.*?)':/g, '"$1":').replace(/'{/g, '{').replace(/\}'/g, '}')));

    // //const locations = JSON.parse('{"lat": 44.372621, "lng": -68.221942}')
    // console.log(locations)
    // console.log(eval(locations))
    // //console.log(JSON.parse("[2017,7,18,9,0]"))
    // console.log("aaaaaaaaaaaaa")

    locations.map((position, i) => {
      
        var poi = new google.maps.LatLng(position[0], position[1]);
        //const label = labels[i % labels.length];
        let num = i
        new google.maps.Marker({
            position: poi,
            map,
            label: num.toString(),
        })
    });

    // const flightPlanCoordinates = [
    //    { lat: 44.372621, lng: -68.221942 },
    //    { lat: 44.35079167, lng: -68.30218833 },
    //    { lat: 44.23383331298821, lng: -68.3199996948242 },
    //    { lat: 44.2284927368164, lng: -68.3237609863281 },
    //    { lat: 44.350011499069, lng: -68.2414535993951 },
    //    { lat: 44.3585023529493, lng: -68.2059851525353 },
    //    { lat: 44.3300018310546, lng: -68.1775283813476 },


    // ];
    // const flightPath = new google.maps.Polyline({
    //     path: locations,
    //     geodesic: true,
    //     strokeColor: "#0000FF",
    //     strokeOpacity: 1.0,
    //     strokeWeight: 2,
    // });

    //flightPath.setMap(map);

directionsRenderer.setMap(map)

calcRoute(directionsService, directionsRenderer, locations)
}


function calcRoute(directionsService, directionsRenderer, locations) {
  const waypts = [];

  for (let i = 1; i < locations.length-1; i++) {
      console.log(i)
      waypts.push({
        location: new google.maps.LatLng(locations[i][0], locations[i][1]),
        stopover: true,
      });
  }
  console.log(waypts)

  directionsService
    .route({
      origin: new google.maps.LatLng(locations[0][0], locations[0][1]),
      destination: new google.maps.LatLng(locations[locations.length-1][0], locations[locations.length-1][1]),
      waypoints: waypts,
      optimizeWaypoints: true,
      travelMode: google.maps.TravelMode.DRIVING,
    })
    .then((response) => {
      directionsRenderer.setDirections(response);
})
}


window.initMap = initMap;
