
var spin_loader = `
<div class="loader loader--style3" title="2">
  <svg version="1.1" id="loader-1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
     width="40px" height="40px" viewBox="0 0 50 50" style="enable-background:new 0 0 50 50;" xml:space="preserve">
  <path class = "loader" fill="#000" d="M43.935,25.145c0-10.318-8.364-18.683-18.683-18.683c-10.318,0-18.683,8.365-18.683,18.683h4.068c0-8.071,6.543-14.615,14.615-14.615c8.072,0,14.615,6.543,14.615,14.615H43.935z">
    <animateTransform attributeType="xml"
      attributeName="transform"
      type="rotate"
      from="0 25 25"
      to="360 25 25"
      dur="0.6s"
      repeatCount="indefinite"/>
    </path>
  </svg>
</div>
`

var token = "pk.eyJ1Ijoia2lyaWxsNDU2eiIsImEiOiJja3kxc3BlbGswOXY3MnJueTdtNDJ5bG8xIn0.qbnJrnDNsML_nlCeFhE-dQ"
var map = L.map('map').setView([55.752101, 37.620923], 13);
var url = window.location.href
console.log(window.location.href)

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + token, {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'your.mapbox.access.token'
}).addTo(map);

var myIcon = L.divIcon({
    iconSize: [30, 30],
    iconAnchor: [15, 15],
    popupAnchor: [10, 0],
    shadowSize: [0, 0],
    className: 'my-div-icon',
    html: spin_loader
});
var loading_marker = L.marker([55.752101, 37.620923], {icon: myIcon})

var polyline = L.polyline([], {color : "#FF6700"})
polyline.addTo(map);

function onMapClick(e) {
    url = new URL(url + 'map');
    params = {lat : e.latlng.lat, lon : e.latlng.lng};
    url.search  = new URLSearchParams(params).toString();
    loading_marker
        .setLatLng(e.latlng)
        .addTo(map);
    fetch(url)
    .then( response => {
        console.log(response);
        return response.json();
    })
    .then( res => {
        loading_marker.removeFrom(map)
        console.log(res)
        //polyline.setStyle({stroke : "#FF6700"})
        polyline.setLatLngs(res);
    })

}

map.on('click', onMapClick);

