const passField = document.getElementById("SecretPassword")

let topSecretPassword = "";
passField.addEventListener("blur", () => {
	topSecretPassword = passField.textContent
})

snapshotCafeData.addEventListener("mouseup", () => { 
	getCafeJSON(); 
});

async function create_cafe(name, positionx, positiony, address, coffee, size, price, matcha, chai, notes) {
	let response = await fetch("/create_cafe", {
		method : "POST",
		headers : {
			"Content-type": "application/json; charset=UTF-8"
		}, 
		body : JSON.stringify({
			password: topSecretPassword,
			cafe: {
				name: name,
				positionx: positiony,
				positiony: positionx,
				size: size,
				coffee: coffee,
				address: address,
				price: price,
				matcha: matcha,
				chai: chai,
				notes: notes
			}
		})
	})
	let data = await response.json()
	document.getElementById("cafeCreated").value = `${data}`
}

async function delete_cafe(cafename) {
	console.log(`deleting cafe ${cafename}`)
	let response = await fetch("/delete_cafe", {
		method : "POST",
		headers : {
			"Content-type": "application/json; charset=UTF-8"
		}, 
		body : JSON.stringify({
			password: topSecretPassword,
			cafe: {
				name: cafename
			}
		})
	})
	return (await response.json()).status == "success";
}

async function modify_cafe(target, name, positionx, positiony, size, coffee, address, price, matcha, chai, notes) {
	let response = await fetch("/modify_cafe", {
		method : "POST",
		headers : {
			"Content-type": "application/json; charset=UTF-8"
		}, 
		body : JSON.stringify({
			password : topSecretPassword,
			cafe : {
				target : target,
				name : name,
				positionx : positionx,
				positiony : positiony,
				size : size,
				coffee : coffee,
				address : address,
				price : price,
				matcha : matcha,
				chai : chai,
				notes : notes
			}
		})
	})
	let data = await response.json();
	const responseText = document.getElementById(`${target}-responseText`)
	responseText.innerText = `status: ${data.status}`
}

async function delete_target_cafe() {
	if (cafeDeleteConfirmation) {
		const cafeTarget = cafeDeleteConfirmation.getAttribute('data-target-cafe');
		if (await delete_cafe(cafeTarget)) {
			const cafeDiv = document.querySelector(`#${cafeTarget}-cafeDiv`)
			cafeDiv.remove();
		} else {
			const responseText = document.getElementById(`${cafeTarget}-responseText`);
			responseText.innerText = `Failed to delete cafe`;
		}
	}
	else {
		console.error("cafeDeleteConfirmation is equal to: ", cafeDeleteConfirmation);
	}
}

async function cafe_delete_listener(event) {
	let locationArray = event.target.id.split("-")
	locationArray.pop()
	const location = locationArray.join("-")
	cafeDeleteConfirmation.setAttribute("data-target-cafe", location)
}

async function cafe_modify_listener(event) {
	let locationArray = event.target.id.split("-")
	locationArray.pop()
	const cafeLocation = locationArray.join("-")
	const name = document.getElementById(`${cafeLocation}-name`)
	const positionx = document.getElementById(`${cafeLocation}-positionx`)
	const positiony = document.getElementById(`${cafeLocation}-positiony`)
	const address = document.getElementById(`${cafeLocation}-address`)
	const coffee = document.getElementById(`${cafeLocation}-coffee`)
	const size = document.getElementById(`${cafeLocation}-size`)
	const price = document.getElementById(`${cafeLocation}-price`)
	const matcha = document.getElementById(`${cafeLocation}-matcha`)
	const chai = document.getElementById(`${cafeLocation}-chai`)
	const notes = document.getElementById(`${cafeLocation}-notes`)
	console.log(`modifying with ${name}, ${positionx}, ${positiony}, ${address}, ${coffee}, ${size}, ${price}, ${matcha}, ${chai}, ${notes}`)
	await modify_cafe(cafeLocation, name.value, positionx.value, positiony.value, size.value, coffee.value, address.value, price.value, matcha.value, chai.value, notes.value)
	const new_location = name.value
	name.id = new_location + "-name"
	positionx.id = new_location + "-positionx"
	positiony.id = new_location + "-positiony"
	address.id = new_location + "-address"
	coffee.id = new_location + "-coffee"
	size.id = new_location + "-size"
	price.id = new_location + "-price"
	matcha.id = new_location + "-matcha"
	chai.id = new_location + "-chai"
	notes.id = new_location + "-notes"
	event.target.id = new_location + "-button"
}

async function getCafeJSON() {
	const cafeData = await fetch(
		"/cafes", {
			method : "GET", 
			headers : {
				"Content-type": "application/json; charset=UTF-8"
			}
		}
	);
	const data = await cafeData.json();
	if ("cafes" in data) {
		const cafes_json = {};
		cafes_json.cafes = [];
		for (const cafeData of data["cafes"]) {
			const item_json = {
				name : cafeData[0],
				longtitude : cafeData[1],
				latitude : cafeData[2],
				address : cafeData[3],
				coffee : cafeData[4],
				size : cafeData[5],
				price : cafeData[6],
				matcha : cafeData[7],
				chai : cafeData[8],
				notes : cafeData[9]
			};
			cafes_json.cafes.push(item_json);
		}

		const json_file_content = JSON.stringify(cafes_json);
		const file_blob = new Blob([json_file_content], { type: "text/plain" });

		const temp_download_link = document.createElement('a');
		temp_download_link.href = URL.createObjectURL(file_blob);
		temp_download_link.download = `${Date.now()}-cafe-data-export.json`;

		temp_download_link.click();
		URL.revokeObjectURL(temp_download_link.href);
	}
	else {
		alert("Unable to snapshot data currently.");
	}
}


function addCafeEditField(cafeData) {
	const newCafeEdit = document.createElement("div")
	newCafeEdit.id = `${cafeData[0]}-cafeDiv`
	newCafeEdit.className = `cafeDiv`
	const cafeInfo = `<label for = "${cafeData[0]}-name">Name:</label>` + `<input type = "text" id = "${cafeData[0]}-name" value = "${cafeData[0]}"/>` + 
		`<label for = "${cafeData[0]}-positionx">Longtitude:</label>` + `<input type = "text" id = "${cafeData[0]}-positionx" value = "${cafeData[1]}"/>` + 
		`<label for = "${cafeData[0]}-positiony">Latitude:</label>` + `<input type = "text" id = "${cafeData[0]}-positiony" value = "${cafeData[2]}"/>` + 
		`<label for = "${cafeData[0]}-address">Address:</label>` + `<input type = "text" id = "${cafeData[0]}-address" value = "${cafeData[5]}"/>` + 
		`<label for = "${cafeData[0]}-coffee">Coffee:</label>` + `<input type = "text" id = "${cafeData[0]}-coffee" value = "${cafeData[4]}"/>` + 
		`<label for = "${cafeData[0]}-size">Size:</label>` + `<input type = "text" id = "${cafeData[0]}-size" value = "${cafeData[3]}"/>` + 
		`<label for = "${cafeData[0]}-price">Price:</label>` + `<input type = "text" id = "${cafeData[0]}-price" value = "${cafeData[6]}"/>` + 
		`<label for = "${cafeData[0]}-matcha">Matcha:</label>` + `<input type = "text" id = "${cafeData[0]}-matcha" value = "${cafeData[7]}"/>` + 
		`<label for = "${cafeData[0]}-chai">Chai:</label>` + `<input type = "text" id = "${cafeData[0]}-chai" value = "${cafeData[8]}"/>` + 
		`<label for = "${cafeData[0]}-notes">Notes:</label>` + `<textarea id = "${cafeData[0]}-notes">${cafeData[9]}</textarea>`
	newCafeEdit.insertAdjacentHTML('beforeend', cafeInfo)

	const submitButton = document.createElement('button')
	submitButton.id = `${cafeData[0]}-button`
	submitButton.className = `update`
	const submitButtonText = document.createTextNode("Save Cafe")
	submitButton.appendChild(submitButtonText)
	submitButton.addEventListener("click", async (event) => { cafe_modify_listener(event) })

	const deleteButton = document.createElement('button');
	deleteButton.id = `${cafeData[0]}-deletebutton`;
	deleteButton.className = `delete`;
	deleteButton.commandForElement = cafeDeleteConfirmation;
	deleteButton.command = "show-modal";
	const deleteButtonText = document.createTextNode("DELETE Cafe");
	deleteButton.appendChild(deleteButtonText);
	deleteButton.addEventListener("click", async (event) => { cafe_delete_listener(event) });
	
	const responseLabel = document.createElement('div');
	responseLabel.innerText = "Update status: ";
	const responseText = document.createElement('p');
	responseText.id = `${cafeData[0]}-responseText`;
	responseText.innerText = "...";

	newCafeEdit.appendChild(responseLabel);
	newCafeEdit.appendChild(responseText);
	newCafeEdit.appendChild(submitButton);
	newCafeEdit.appendChild(deleteButton);

	const editList = document.getElementById("cafeEditsList");
	editList.appendChild(newCafeEdit);
}

(async() => {
	const cafeData = await fetch(
		"/cafes", {
			method : "GET", 
			headers : {
				"Content-type": "application/json; charset=UTF-8"
			}
		}
	)
	const data = await cafeData.json()
	if ("cafes" in data) {
		for (const cafe of data["cafes"]) {
			addCafeEditField(cafe)
		}
	}
})()

document.getElementById("createCafeButton").addEventListener("click", async () => { 
	create_cafe(
		document.getElementById("CreateCafe-name").value,
		document.getElementById("CreateCafe-positionx").value,
		document.getElementById("CreateCafe-positiony").value,
		document.getElementById("CreateCafe-address").value,
		document.getElementById("CreateCafe-coffee").value,
		document.getElementById("CreateCafe-size").value,
		document.getElementById("CreateCafe-price").value,
		document.getElementById("CreateCafe-matcha").value,
		document.getElementById("CreateCafe-chai").value,
		document.getElementById("CreateCafe-notes").value
	) 
})
