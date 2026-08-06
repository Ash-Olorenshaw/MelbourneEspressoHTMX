
let fontSize = "11px";

function constructPopupHtml(data, type) {
	let popup = ""
	if (type == "cafe") {
		popup = "<p style = \"display:inline; word-wrap: break-word\">" + 
			"<div><span style=\"font:" + fontSize + " Arial\"><h1 style=\"margin-bottom: -10px; margin-top: 0\">" + data[0] + "</h1></br>" +
			"Address: " + data[5] + "</br>" +
			"Coffee: " + data[4] + "</br>" +
			"Size: " + data[3] + "</br>" +
			"Price: " + data[6] + "</br>" +
			"Matcha? " + data[7] + "</br>" +
			"Chai? " + data[8] + "</br>" +
			"Notes: " + data[9] + "</span></br></div></p>";
	}
	else if (type == "toilet") {
		popup = '<p style = "display:inline; word-wrap: break-word">' + 
			'<div><span style="font:' + fontSize + ' Arial"><h1 style="margin-bottom: -10px; margin-top: 0">' + data[0] + "</h1></br>" +
			'Address: ' + data[3] + "</br>" +
			'Notes: ' + data[4] + "</span></br>" +
			'</div></p>'
	}

	return popup
}

async function createToiletMarkers() {
	const response = await fetch("/toilets", {method : "GET", headers : {"Content-type": "application/json; charset=UTF-8"}});
	const data = await response.json();
	const toilets = data["toilets"]

	for (const toilet of toilets) {
		const popup = constructPopupHtml(toilet, "toilet")
		const icon = datacontainer.getAttribute("data-toilet-icon")
		addMapMarker(popup, parseFloat(toilet[2]), parseFloat(toilet[1]), icon)
	}
}

async function createCafeMarkers() {
	const response = await fetch("/cafes", {method : "GET", headers : {"Content-type": "application/json; charset=UTF-8"}})
	const data = await response.json()
	const cafes = data["cafes"]

	for (const cafe of cafes) {
		const popup = constructPopupHtml(cafe, "cafe")
		const icon = datacontainer.getAttribute("data-cup-icon")
		addMapMarker(popup, parseFloat(cafe[2]), parseFloat(cafe[1]), icon)
	}
}

const delay = ms => new Promise(res => setTimeout(res, ms));

async function updateMarks() {
	const cafeToggle = document.getElementById("cafeSwitch");
	const toiletToggle = document.getElementById("toiletSwitch");

	clearMapMarks();

	if (cafeToggle.checked)
		createCafeMarkers();
	
	if (toiletToggle.checked)
		createToiletMarkers();
}

(async() => {
	updateMarks();
})()


