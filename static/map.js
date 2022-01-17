
var token = "pk.eyJ1Ijoia2lyaWxsNDU2eiIsImEiOiJja3kxc3BlbGswOXY3MnJueTdtNDJ5bG8xIn0.qbnJrnDNsML_nlCeFhE-dQ"
var map = L.map('map').setView([51.505, -0.09], 13);
var url = "http://192.168.0.102:5000/"

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + token, {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'your.mapbox.access.token'
}).addTo(map);

var popup = L.popup();
var polyline = L.polyline({color : 'red'}).addTo(map);

function onMapClick(e) {
    url = new URL(url + 'map');
    params = {lat : e.latlng.lat, lon : e.latlng.lng};
    url.search  = new URLSearchParams(params).toString();
    popup
        .setLatLng(e.latlng)
        .setContent("Fetching...")
        .openOn(map);
    fetch(url)
    .then( response => {
        popup.setContent("Plotting...")
        console.log(response);
        return response.json();
    })
    .then( res => {
        console.log(res)
        polyline.setLatLngs(res);
    })

}

map.on('click', onMapClick);

