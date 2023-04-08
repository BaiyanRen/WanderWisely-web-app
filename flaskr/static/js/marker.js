
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

    console.log("aaaaaaaaaaaaa")
    const locations = JSON.parse(document.getElementById('locations').getAttribute("locations"))
    console.log(locations)
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

    flightPath.setMap(map);

}



window.initMap = initMap;
