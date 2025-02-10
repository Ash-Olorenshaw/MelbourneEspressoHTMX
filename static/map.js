var map
var cafeMarks = []
let locationOn = false
let locationMark = null

map = L.map('map').setView([-37.8130830335284, 144.96277203427053], 15.0)

// Add the tile layer from OpenStreetMap
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {//https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png', {
	maxZoom: 19,
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map)

function clearMapMarks() {
	for (m of cafeMarks) {
		map.removeLayer(m)
	}
}

function addMapMarker(markerHtml, lat, lng, iconImage) {
	var coffeeIcon = L.icon({
		iconUrl : iconImage, //{{ url_for("static", filename = "images/CupIcon.png") }},
		shadowUrl : "",

		iconSize : [32, 32],
		shadowSize : [0, 0],
		iconAnchor : [0, 0],
		shadowAnchor : [4, 62],
		popupAnchor : [0, 0]
	});
	
	let newMark = new L.marker([lat, lng], {icon : coffeeIcon}).addTo(map);
	newMark.bindPopup(markerHtml, {maxWidth : 500})
	cafeMarks.push(newMark);
}

function displayUserLocation() {
	if (locationOn) {
		if (locationMark != null) {
			map.removeLayer(locationMark)
		}
		navigator.geolocation.getCurrentPosition(position => {
			const { coords: { latitude, longitude }} = position;
			locationMark = new L.marker([latitude, longitude], {}).addTo(map)
		})	
	}
}

const collectUserLocation = setInterval(function() {
	displayUserLocation()
}, 5000);


function switchLocationOn() {
	locationOn = !locationOn
	if (locationOn) {
		collectUserLocation
	} else {
		clearInterval(collectUserLocation)
		map.removeLayer(locationMark)
	}
}

